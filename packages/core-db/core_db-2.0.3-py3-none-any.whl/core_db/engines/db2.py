# -*- coding: utf-8 -*-

from pyodbc import connect

from core_db.interfaces.base import DatabaseClientException
from core_db.interfaces.sql_based import SqlDatabaseClient


class Db2Client(SqlDatabaseClient):
    """
    Client for IBM DB2 database connection...

    ===================================================
    How to use
    ===================================================

    driver = "IBM i Access ODBC Driver 64-bit"
    host, port = "SOME_HOST", 1521

    WITH Context Manager
    ---------------------------------------------------

        with Db2Client(
                dsn=f"DRIVER={driver};SYSTEM={host};PORT={port};",
                user=username, password=password, ssl=False ) as client:

            client.execute("select...")
            res = list(client.fetch_records())
            print(res)

    WITHOUT Context Manager
    ---------------------------------------------------

        client = Db2Client(dsn=DSN, user=username, password=password, ssl=False)
        client.connect()

        res = client.test_connection()
        print(res)

        cursor = client.execute("select ...")
        res = client.fetch_records()
        print(list(res))
        client.close()
        print(res)

    ===================================================
    Driver Installation
    Debian-based and Ubuntu-based Distributions
    ===================================================

    curl https://public.dhe.ibm.com/software/ibmi/products/odbc/debs/dists/1.1.0/ibmi-acs-1.1.0.list | sudo tee /etc/apt/sources.list.d/ibmi-acs-1.1.0.list
    sudo apt update
    sudo apt install ibm-iaccess

    More information:
    https://ibmi-oss-docs.readthedocs.io/en/latest/odbc/installation.html
    """

    def __init__(self, **kwargs):
        super(Db2Client, self).__init__(**kwargs)
        self.connect_fcn = connect

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    def connect(self) -> None:
        try:
            self.cxn = self.connect_fcn(
                self.cxn_parameters.pop("dsn", ""),
                **self.cxn_parameters)

        except Exception as error:
            raise DatabaseClientException(error)

    def test_connection(self, query: str = None):
        return super(Db2Client, self)\
            .test_connection(query or "SELECT * FROM SYSIBMADM.ENV_SYS_INFO")\
            .fetchone()
