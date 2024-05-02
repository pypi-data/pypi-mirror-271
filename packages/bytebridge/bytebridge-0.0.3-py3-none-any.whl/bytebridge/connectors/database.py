from contextlib import closing
from typing import Callable, Dict, Iterator, List, Optional

import mysql.connector
import psycopg
import pymssql
from psycopg.rows import dict_row

from bytebridge.connectors.base import Connector


class DatabaseConnector(Connector):
    def __init__(
        self,
        *,
        connection_handler: Callable,
        connection_parameters: Dict,
        cursor_parameters: Dict,
    ) -> None:
        self._connection_handler = connection_handler
        self._connection_parameters = connection_parameters
        self._cursor_parameters = cursor_parameters

    def extract(
        self,
        *,
        source_object: Optional[str],
        source_query: Optional[str],
        batch_size: int,
    ):
        sql = self._render_query(source_query, source_object)

        with closing(
            self._connection_handler(
                host=self._connection_parameters["host"],
                user=self._connection_parameters["user"],
                password=self._connection_parameters["password"],
                port=self._connection_parameters["port"],
            ),
        ) as connection:
            with closing(connection.cursor(**self._cursor_parameters)) as cursor:
                cursor.execute(sql)
                while True:
                    batch = cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    yield batch

    def load(
        self,
        *,
        batch_iterator: Iterator[List[dict]],
        target_object: str,
    ):
        batch = next(batch_iterator)
        if batch:
            column_names = batch[0].keys()
            with closing(
                self._connection_handler(
                    host=self._connection_parameters["host"],
                    user=self._connection_parameters["user"],
                    password=self._connection_parameters["password"],
                    port=self._connection_parameters["port"],
                    autocommit=True,
                ),
            ) as connection:
                with closing(connection.cursor(**self._cursor_parameters)) as cursor:
                    sql = self._generate_insert_statement(
                        target_table=target_object,
                        column_names=column_names,
                    )
                    cursor.executemany(
                        sql,
                        self._generate_list_of_tuples_from_list_of_dictionaries(batch),
                    )
                    for batch in batch_iterator:
                        cursor.executemany(
                            sql,
                            self._generate_list_of_tuples_from_list_of_dictionaries(
                                batch
                            ),
                        )

    def _generate_insert_statement(self, target_table: str, column_names: List[str]):
        return f"""
                INSERT INTO {target_table} ({",".join(column_names)})
                VALUES ({",".join(["%s" for _ in range(len(column_names))])})
        """

    def _generate_list_of_tuples_from_list_of_dictionaries(self, list: dict):
        return [tuple(value.values()) for value in list]

    def _render_query(self, query: str, object: str) -> str:
        sql = None
        if query:
            if query.endswith((".sql",)):
                with open(query) as file:
                    sql: str = file.read()
        elif object:
            sql = f"SELECT * FROM {object};"

        return sql


class PostgresConnector(DatabaseConnector):
    def __init__(self, *, connection_parameters: dict) -> None:
        self._connection_handler = psycopg.connect
        self._cursor_parameters = {"row_factory": dict_row}
        self._connection_parameters = connection_parameters


class MySqlConnector(DatabaseConnector):
    def __init__(self, *, connection_parameters: dict) -> None:
        self._connection_handler = mysql.connector.connect
        self._cursor_parameters = {"dictionary": True}
        self._connection_parameters = connection_parameters


class MsSqlConnector(DatabaseConnector):
    def __init__(self, *, connection_parameters: dict) -> None:
        self._connection_handler = pymssql.connect
        self._cursor_parameters = {"as_dict": True}
        self._connection_parameters = connection_parameters
