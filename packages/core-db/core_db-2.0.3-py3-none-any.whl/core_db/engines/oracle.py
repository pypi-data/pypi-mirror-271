# -*- coding: utf-8 -*-

import oracledb

from core_db.interfaces.sql_based import SqlDatabaseClient


class OracleClient(SqlDatabaseClient):
    """
    Client for Oracle connection...

    ===================================================
    How to use
    ===================================================

    WITHOUT Context Manager
    ---------------------------------------------------

        client = OracleClient(user="...", password="...", dsn=f"{host}:{port}/{service_name}")
        client.connect()

        res = client.execute("SELECT * FROM ...")
        for x in client.fetch_all():
            print(x)
        client.close()


    WITH Context Manager
    ---------------------------------------------------

        with OracleClient(user="...", password="...", dsn=f"{host}:{port}/{service_name}") as client:
            res = client.execute("SELECT * FROM ...")
            for x in client.fetch_all():
                print(x)
    """

    def __init__(self, **kwargs):
        """
        Expected -> user, password, dsn...

        More information:
          - https://oracle.github.io/python-oracledb/
          - https://python-oracledb.readthedocs.io/en/latest/index.html

        """

        super(OracleClient, self).__init__(**kwargs)
        self.connect_fcn = oracledb.connect

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    def test_connection(self, query: str = None):
        if not query:
            query = 'SELECT * FROM "V$VERSION"'

        return super(OracleClient, self).test_connection(query)
