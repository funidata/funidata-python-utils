#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from pathlib import PosixPath
from typing import ClassVar, override

from pydantic import SecretStr, BaseModel, ConfigDict, model_validator

from .source_config import SourceConfig
from ..database.db_util import get_engine, get_by_statement


UNSET_DEFAULT = b'x_unset'


class DatabaseConfig(SourceConfig):
    """
        If `override_connection_uri` is configured, that will take presedence over the other parameters.
        Otherwise, engine will be constructed according to connection template.
        connect_args dict is always passed to engine connect args, regardless of connection uri initialization method.
    """
    name: ClassVar[str] = 'base-database-config'
    connection_template: str = "{sql_server_type}+{sql_driver}://{uname}:{pwd}@{host}:{port}/{database}"

    override_connection_uri: SecretStr | None = None
    host: str | None = UNSET_DEFAULT
    sql_server_type: str | None = UNSET_DEFAULT
    sql_driver: str | None = UNSET_DEFAULT
    username: str | None = UNSET_DEFAULT
    password: SecretStr | None = UNSET_DEFAULT
    port: int | None = UNSET_DEFAULT
    database: str | None = UNSET_DEFAULT

    connect_args: dict | None = None

    @model_validator(mode='after')
    def override_or_params_required(self):
        if self.override_connection_uri:
            return self

        if any(
            x == UNSET_DEFAULT
                for x in {self.host, self.sql_driver, self.sql_server_type, self.username, self.password, self.port, self.database}
        ):
            raise ValueError('Explicitly define config parameters when not using override_connection_uri')

        return self

    def get_connection_uri(self) -> str:
        if self.override_connection_uri:
            return self.override_connection_uri.get_secret_value()

        return self.connection_template.format(
            uname=self.username,
            pwd=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database,
            sql_server_type=self.sql_server_type,
            sql_driver=self.sql_driver,
        )

    def _get_connect_args(self) -> dict:
        if not self.connect_args:
            return {}

        return self.connect_args

    def get_engine(self):
        return get_engine(
            self.get_connection_uri(),
            connect_args=self._get_connect_args() or {}
        )

    def get_by_statement(self, stmt: str, sql_params_dict: dict | None = None):
        with self.get_engine().connect() as connection:
            with connection.begin():
                return get_by_statement(
                    connection,
                    stmt,
                    sql_params_dict
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
    def get_by_statement(self, stmt: str, sql_params_dict: dict | None = None):
        return []


class PyMySqlSslConnectArgs(BaseModel):
    model_config = ConfigDict(extra='allow')

    ca: PosixPath | None = None
    cert: PosixPath | None = None
    key: PosixPath | None = None
    verify_cert: bool | None = None
    verify_identity: bool | None = None
    check_hostname: bool | None = None


class PymySqlConnectArgs(BaseModel):
    model_config = ConfigDict(extra='allow')

    ssl: PyMySqlSslConnectArgs | None = None


class MariaDbConfig(DatabaseConfig):
    name: ClassVar[str] = 'mariadb-sql'
    connection_template: str = "{sql_server_type}+{sql_driver}://{uname}:{pwd}@{host}:{port}/"
    override_connection_uri: SecretStr | None = None
    sql_server_type: str = 'mariadb'
    sql_driver: str = 'pymysql'
    username: str | None = UNSET_DEFAULT
    password: SecretStr | None = UNSET_DEFAULT
    port: int | None = UNSET_DEFAULT
    database: None = None

    connect_args: PymySqlConnectArgs | None = None

    @override
    def _get_connect_args(self) -> dict:
        if not self.connect_args:
            return {}

        return self.connect_args.model_dump(exclude_none=True)
