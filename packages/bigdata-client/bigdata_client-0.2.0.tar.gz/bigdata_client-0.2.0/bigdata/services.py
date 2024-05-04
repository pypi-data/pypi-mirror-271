import os
import time
from datetime import datetime
from typing import List, Optional, Union

import requests

from bigdata import old_auth
from bigdata.api.knowledge_graph import (
    AutosuggestRequests,
    AutosuggestResponse,
    ByIdsRequest,
)
from bigdata.api.uploads import ExtractorTypes, PostFileRequest
from bigdata.api.watchlist import CreateWatchlistRequest, UpdateWatchlistRequest
from bigdata.auth import Auth
from bigdata.connection import BigdataConnection, UploadsConnection, upload_file
from bigdata.connection_protocol import BigdataConnectionProtocol
from bigdata.daterange import AbsoluteDateRange, RollingDateRange
from bigdata.file_status import FileStatus
from bigdata.models.advanced_search_query import QueryComponent
from bigdata.models.entities import MacroEntity
from bigdata.models.languages import Language
from bigdata.models.parse import (
    AutosuggestedSavedSearch,
    EntityTypes,
    KnowledgeGraphTypes,
)
from bigdata.models.search import FileType, SortBy
from bigdata.models.sources import Source
from bigdata.models.topics import Topic
from bigdata.models.uploads import File
from bigdata.models.watchlists import Watchlist
from bigdata.pdf_utils import is_pdf_file
from bigdata.query_type import QueryType
from bigdata.search import Search
from bigdata.settings import BigdataAuthType, settings

CONCURRENT_AUTOSUGGEST_REQUESTS_LIMIT = 10


class Bigdata:
    """
    Represents a connection to RavenPack's Bigdata API.

    :ivar knowledge_graph: Proxy for the knowledge graph search functionality.
    :ivar content_search: Proxy object for the content search functionality.
    :ivar watchlists: Proxy object for the watchlist functionality.
    :ivar uploads: Proxy object for the internal content functionality.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_type: Optional[BigdataAuthType] = None,
        bigdata_api_url: Optional[str] = None,
        upload_api_url: Optional[str] = None,
    ):
        if password is None:
            password = os.environ.get("BIGDATA_PASSWORD")
        if username is None:
            username = os.environ.get("BIGDATA_USER")
        if username is None or password is None:
            raise ValueError("Username and password must be provided")
        if auth_type is None:
            auth_type = settings.BIGDATA_AUTH_TYPE
        if auth_type == BigdataAuthType.CLERK:
            auth = Auth.from_username_and_password(username, password)
        else:
            auth = old_auth.Auth.from_username_and_password(username, password)

        if bigdata_api_url is None:
            bigdata_api_url = str(settings.BIGDATA_API_URL)
        if upload_api_url is None:
            upload_api_url = str(settings.UPLOAD_API_URL)

        self._api = BigdataConnection(auth, bigdata_api_url)
        self._upload_api = UploadsConnection(auth, upload_api_url)
        self.knowledge_graph = KnowledgeGraph(self._api)
        self.content_search = ContentSearch(self._api)
        self.watchlists = Watchlists(self._api)
        self.uploads = Uploads(self._upload_api)


class KnowledgeGraph:
    """For finding entities, sources and topics"""

    def __init__(self, api_connection: BigdataConnectionProtocol):
        self._api = api_connection

    def autosuggest(
        self, values: list[str], /, limit=20
    ) -> dict[str, list[KnowledgeGraphTypes]]:
        """
        Searches for entities, sources, topics, searches and watchlists
        Args:
            values: Searched items
            limit: Upper limit for each result

        Returns:
            Dictionary with the searched terms as keys each with a list of results.
        """

        api_response = self._api.autosuggest(
            AutosuggestRequests(root=values),
            limit=limit,
        )

        # Exclude macros and saved searches from response
        api_response = self._exclude_macros_and_saved_searches(api_response)

        return {key: results for key, results in api_response.root.items()}

    @staticmethod
    def _exclude_macros_and_saved_searches(
        api_response: AutosuggestResponse,
    ) -> AutosuggestResponse:
        filtered_response = {}
        for key, key_results in api_response.root.items():
            filtered_response[key] = list(
                filter(
                    lambda result: not isinstance(
                        result, (MacroEntity, AutosuggestedSavedSearch)
                    ),
                    key_results,
                )
            )
        return AutosuggestResponse(root=filtered_response)

    def get_entities(self, ids: list[str], /) -> list[Optional[EntityTypes]]:
        """Retrieve a list of entities by their ids."""
        return self._get_by_ids(ids, QueryType.ENTITY)

    def get_sources(self, ids: list[str], /) -> list[Optional[Source]]:
        """Retrieve a list of sources by its ids."""
        return self._get_by_ids(ids, QueryType.SOURCE)

    def get_topics(self, ids: list[str], /) -> list[Optional[Topic]]:
        """Retrieve a list of topics by its ids."""
        return self._get_by_ids(ids, QueryType.TOPIC)

    def get_languages(self, ids: list[str], /) -> list[Optional[Language]]:
        """Retrieve a list of languages by its ids."""
        return self._get_by_ids(ids, QueryType.LANGUAGE)

    def _get_by_ids(self, ids: list[str], query_type: QueryType) -> list:
        api_response = self._api.by_ids(
            ByIdsRequest.model_validate(
                [{"key": id_, "queryType": query_type} for id_ in ids]
            )
        )
        return [api_response.root.get(id_) for id_ in ids]


class Watchlists:
    """For finding, iterating and doing operations with watchlist objects"""

    def __init__(self, api_connection: BigdataConnectionProtocol):
        self._api = api_connection

    def get(self, id_: str, /) -> Watchlist:
        """Retrieve a watchlist by its id."""
        api_response = self._api.get_single_watchlist(id_)
        watchlist = Watchlist(
            id=api_response.id,
            name=api_response.name,
            date_created=api_response.date_created,
            last_updated=api_response.last_updated,
            items=api_response.items,
            # Keep track of the api_connection within the Watchlist instance
            _api=self._api,
        )

        return watchlist

    def list(self) -> list[Watchlist]:
        """Retrieve all watchlist objects for the current user."""
        api_response = self._api.get_all_watchlists()
        all_watchlist = [
            Watchlist(
                id=base_watchlist.id,
                name=base_watchlist.name,
                date_created=base_watchlist.date_created,
                last_updated=base_watchlist.last_updated,
                items=None,
                # Keep track of the api_connection within the Watchlist instance
                _api=self._api,
            )
            for base_watchlist in api_response.root
        ]

        return all_watchlist

    def create(self, name: str, items: List[str]) -> Watchlist:
        """Creates a new watchlist in the system."""
        api_response = self._api.create_watchlist(
            CreateWatchlistRequest(name=name, items=items)
        )
        return Watchlist(
            id=api_response.id,
            name=api_response.name,
            date_created=api_response.date_created,
            last_updated=api_response.last_updated,
            items=api_response.items,
            # Keep track of the api_connection within the Watchlist instance
            _api=self._api,
        )

    def delete(self, id_: str, /) -> str:
        """Delete a watchlist by its id."""
        api_response = self._api.delete_watchlist(id_)
        return api_response.id

    def update(self, id_: str, /, name=None, items=None) -> Watchlist:
        """Update a watchlist by its id."""
        api_response = self._api.patch_watchlist(
            id_, UpdateWatchlistRequest(name=name, items=items)
        )
        return Watchlist(
            id=api_response.id,
            name=api_response.name,
            date_created=api_response.date_created,
            last_updated=api_response.last_updated,
            items=api_response.items,
            # Keep track of the api_connection within the Watchlist instance
            _api=self._api,
        )


class ContentSearch:
    def __init__(self, api_connection: BigdataConnection):
        self._api = api_connection

    def new_from_query(
        self,
        query: QueryComponent,
        date_range: Optional[Union[AbsoluteDateRange, RollingDateRange]] = None,
        sortby: SortBy = SortBy.RELEVANCE,
        scope: FileType = FileType.ALL,
    ) -> Search:
        """
        Creates a new search object that allows you to perform a search on
        keywords, entities, etc.

        Example usage:

        >>> query = Entity("228D42") & Keyword("tesla")  # doctest: +SKIP
        >>> search = bigdata.content_search.new_from_query(
        ...    query,
        ...    date_range=RrollingDateRange.LAST_WEEK,
        ...    sortby=SortBy.RELEVANCE,
        ...    scope=FileType.ALL
        ... )                               # doctest: +SKIP
        >>> search.save()                   # doctest: +SKIP
        >>> for story in search.limit(100): # doctest: +SKIP
        >>>     print(story)                # doctest: +SKIP
        >>> print(search.get_summary())     # doctest: +SKIP
        >>> search.delete()                 # doctest: +SKIP
        """
        return Search.from_query(
            self._api, query, date_range=date_range, sortby=sortby, scope=scope
        )

    def get(self, id_, /) -> Search:
        """Retrieve a saved search by its id."""
        response = self._api.get_search(id_)
        return Search.from_saved_search_response(self._api, response)

    def list(self) -> list[Search]:
        """Retrieve all saved searches for the current user."""
        list_response = self._api.list_searches()
        searches = []
        for search in list_response.results:
            try:
                response = self._api.get_search(search.id)
            except NotImplementedError as e:
                print(
                    f"Skipping search {search.id} because it has an unsupported expression type"
                )
                continue
            searches.append(Search.from_saved_search_response(self._api, response))
        return searches

    def delete(self, id_, /):
        """Delete a saved search by its id."""
        self._api.delete_search(id_)


class Uploads:
    """For managing internal uploads. Searching will be done through content"""

    def __init__(self, api_connection: UploadsConnection):
        self._api = api_connection

    def get(self, id_, /) -> File:
        """Retrieve a file by its id."""
        response = None
        while response is None:
            try:
                response = self._api.get_file(id_)
            except requests.exceptions.HTTPError as e:
                # While unavailable, keep trying
                if e.response.status_code == 425:
                    time.sleep(1)
                    continue
                raise e
        return File(
            _api=self._api,
            id=response.id,
            name=response.name,
            status=response.status,
            uploaded_at=response.uploaded_at,
            raw_size=response.raw_size,
            folder_id=response.folder_id,
            trashed=response.trashed,
            starred=response.starred,
            tags=response.tags,
        )

    def list(
        self,
        start_date: Optional[Union[datetime, str]] = None,
        end_date: Optional[Union[datetime, str]] = None,
        tags: Optional[list[str]] = None,
        status: Optional[FileStatus] = None,
        file_name: Optional[str] = None,
        folder_id: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> list[File]:
        """Retrieve all documents for the current user."""
        date_range = (
            AbsoluteDateRange(start_date, end_date) if start_date or end_date else None
        )
        response = self._api.list_files(
            date_range=date_range,
            tags=tags,
            status=status,
            file_name=file_name,
            folder_id=folder_id,
            page_size=page_size,
        )
        docs = []
        for upload in response.results:
            doc = File(
                _api=self._api,
                id=upload.id,
                name=upload.name,
                status=upload.status,
                uploaded_at=upload.uploaded_at,
                raw_size=upload.raw_size,
                folder_id=upload.folder_id,
                trashed=upload.trashed,
                starred=upload.starred,
                tags=upload.tags,
            )
            docs.append(doc)

        return docs

    def upload_from_disk(
        self,
        path: str,
        /,
        provider_document_id: Optional[str] = None,
        provider_date_utc: Optional[Union[str, datetime]] = None,
    ) -> File:
        """Uploads a file to the bigdata platform."""
        filename = os.path.basename(path)

        properties = {}
        if provider_document_id is not None:
            properties["provider_document_id"] = provider_document_id
        if provider_date_utc is not None:
            if isinstance(provider_date_utc, datetime):
                provider_date_utc = provider_date_utc.strftime("%Y-%m-%d %H:%M:%S")
            properties["provider_date_utc"] = provider_date_utc
        if is_pdf_file(path):
            properties["extractor"] = ExtractorTypes.PDF_EXTRACTOR_1_0
        properties = properties or None

        # Pre-upload
        post_file_request = PostFileRequest(
            filename=filename,
            folder_id=None,
            source_url=None,
            upload_mode=None,
            properties=properties,
        )
        post_file_request = self._api.post_file(post_file_request)

        with open(path, "rb") as file:
            upload_file(post_file_request.location, file)
        return self.get(post_file_request.file_id)

    def delete(self, id_, /):
        """Delete a file by its id."""
        self._api.delete_file(id_)
