# -*- coding: utf-8 -*-

from abc import ABC
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Self
from typing import Type

from core_mixins.interfaces.factory import IFactory


class DatabaseClient(IFactory, ABC):
    """ Base class for all database clients """

    _impls: Dict[str, Type[Self]] = {}

    # Mapper for python types to database types...
    type_mapper = {}

    def __init__(self, **kwargs):
        self.cxn_parameters = kwargs
        self.cursor = None
        self.cxn = None

        # Function used by the library to perform
        # the connection to the engine...
        self.connect_fcn = None

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def connect(self) -> None:
        """ It creates the connection """

        try:
            self.cxn = self.connect_fcn(**self.cxn_parameters)

        except Exception as error:
            raise DatabaseClientException(error)

    def test_connection(self, query: str):
        """ Tests the connection """

    def commit(self) -> None:
        """ It applies the changes """

    def fetch_records(self) -> Iterator[Dict[str, Any]]:
        """ Returns the records """

    def close(self):
        """ It releases resources """

        if self.cxn:
            self.cxn.close()


class DatabaseClientException(Exception):
    """ Custom exception for Database Client """
