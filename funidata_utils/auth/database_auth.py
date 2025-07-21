#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import ClassVar, override

from pydantic import SecretStr

from .source_config import SourceConfig
from ..database.db_util import get_engine, get_by_statement


class DatabaseConfig(SourceConfig):
    name: ClassVar[str] = 'base-database-config'
    connection_template: str = "{sql_server_type}+{sql_driver}://{uname}:{pwd}@{host}:{port}/{database}"

    sql_server_type: str
    sql_driver: str
    username: str
    password: SecretStr
    port: int
    database: str

    def get_connection_uri(self):
        return self.connection_template.format(
            uname=self.username,
            pwd=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database,
            sql_server_type=self.sql_server_type,
            sql_driver=self.sql_driver,
        )

    def get_engine(self):
        return get_engine(
            self.get_connection_uri(),
            connect_args={}
        )

    def get_by_statement(self, stmt: str):
        with self.get_engine().connect() as connection:
            with connection.begin():
                return get_by_statement(
                    connection,
                    stmt
                )


class MockDbConfig(DatabaseConfig):
    name: ClassVar[str] = 'mock-db'
    sql_server_type: str = 'mockdb'
    sql_driver: str = 'mockdriver'
    username: str
    password: SecretStr
    port: int
    database: str

    @override
    def get_by_statement(self, stmt: str):
        return []


class MariaDbConfig(DatabaseConfig):
    name: ClassVar[str] = 'mariadb-sql'
    connection_template: str = "{sql_server_type}+{sql_driver}://{uname}:{pwd}@{host}:{port}/?ssl_check_hostname=false"
    sql_server_type: str = 'mariadb'
    sql_driver: str = 'pymysql'
    username: str
    password: SecretStr
    port: int
    database: None = None
