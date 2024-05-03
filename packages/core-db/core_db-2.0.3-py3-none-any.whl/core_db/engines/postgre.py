# -*- coding: utf-8 -*-

import json
from typing import Dict, List

import psycopg

from core_db.interfaces.sql_based import SqlDatabaseClient


class PostgreClient(SqlDatabaseClient):
    """
    Client for PostgreSQL connection...

    ===================================================
    How to use
    ===================================================

    WITH Context Manager
    ---------------------------------------------------

        with PostgreClient(conninfo=f"postgresql://postgres:postgres@localhost:5432/test") as client:
            client.execute("SELECT version() AS version;")
            print(client.fetch_one()[0])

    WITHOUT Context Manager
    ---------------------------------------------------

        client = PostgreClient(conninfo=f"postgresql://postgres:postgres@localhost:5432/test")
        client.connect()

        client.execute("SELECT version();")
        print(list(client.fetch_records()))
        client.close()
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.epoch_to_timestamp_fcn = "TO_TIMESTAMP"
        self.connect_fcn = psycopg.connect

    @classmethod
    def registered_name(cls) -> str:
        return cls.__name__

    @staticmethod
    def get_merge_dml(
            table_fqn: str, pk_ids: List[str], columns: List[str],
            records: List[Dict]) -> str:

        rows = [
            str(
                tuple(
                    [
                        json.dumps(value)
                        if type(value) in [dict, list] else value
                        for attr, value in record.items()
                    ]
                )
            ) for record in records
        ]

        set_statement = ", \n".join([f"{column} = EXCLUDED.{column}" for column in columns if column not in pk_ids])
        rows = ", \n".join(rows)

        return f"""
            INSERT INTO {table_fqn} ({', '.join(columns)}) 
            VALUES 
                {rows} 
            ON CONFLICT ({', '.join(pk_ids)}) DO UPDATE 
            SET 
                {set_statement};"""
