"""
Module containing a client that is a abstraction of the MongoClient.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

TIMEOUT: int = 30000

DocumentType = dict[str, Any]


@dataclass(frozen=True)
class DocumentDBAuthentication:
    """
    Dataclass containing authentication values for the Document DB
    """

    username: str
    password: str


class DocumentDBClient:
    """
    Class for a document db client, this client connects with a document database.
    """

    _mongo_client: MongoClient[DocumentType]
    _database: str
    _default_collection: str
    _current_collection: Collection[DocumentType] | None
    _authentication: DocumentDBAuthentication

    def __init__(
        self,
        connection: str,
        database: str,
        default_collection: str,
        authentication: DocumentDBAuthentication,
        tls: bool = True
    ) -> None:
        """
        database: Company PublicId
        collection: Cloud Function PublicId
        """

        self._database = database
        self._default_collection = default_collection
        self._authentication = authentication

        self._mongo_client = MongoClient(
            connection,
            username=self._authentication.username,
            password=self._authentication.password,
            timeoutMS=TIMEOUT,
            tls=tls
        )

        self._current_collection = None

    def insert_one(self, document: DocumentType) -> InsertOneResult:
        """
        Insert a single document.
        """
        return self._get_collection().insert_one(document)

    def insert_many(self, documents: Iterable[DocumentType]) -> InsertManyResult:
        """
        Insert an iterable of documents.
        """
        return self._get_collection().insert_many(documents)

    def update_one(self, filter_map: Mapping[str, Any], update: Mapping[str, Any]) -> UpdateResult:
        """
        Update a single document matching the filter.
        """
        return self._get_collection().update_one(filter_map, update)

    def update_many(self, filter_map: Mapping[str, Any], update: Mapping[str, Any]) -> UpdateResult:
        """
        Update one or more documents that match the filter.
        """
        return self._get_collection().update_many(filter_map, update)

    def delete_one(self, filter_map: Mapping[str, Any]) -> DeleteResult:
        """
        Delete a single document matching the filter.
        """
        return self._get_collection().delete_one(filter_map)

    def delete_many(self, filter_map: Mapping[str, Any]) -> DeleteResult:
        """
        Delete one or more documents matching the filter.
        """
        return self._get_collection().delete_many(filter_map)

    def find_one(
        self, *args: Any, filter_map: Any | None, **kwargs: Any
    ) -> DocumentType | None:
        """
        Get a single document from the database.
        """
        return self._get_collection().find_one(filter_map, *args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> Cursor[DocumentType]:
        """
        Query the database.
        """
        return self._get_collection().find(*args, **kwargs)

    def switch_collection(self, collection_name: str | None) -> None:
        """
        Switch to another collection.

        When collection_name is None or an empty string, the default collection is used
        """
        self._current_collection = None
        self._get_collection(collection_name)

    def _get_collection(self, collection_name: str | None = None) -> Collection[DocumentType]:
        if self._current_collection is not None:
            return self._current_collection

        if collection_name:
            collection_name = f'{self._default_collection}_{collection_name}'

        self._current_collection = self._mongo_client.get_database(self._database).get_collection(
            collection_name or self._default_collection
        )
        return self._current_collection

    def __repr__(self) -> str:
        return (
            '<DocumentDBClient'
            f' database={self._database},'
            f' default_collection={self._default_collection},'
            '>'
        )
