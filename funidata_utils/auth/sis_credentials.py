import getpass
from typing import Tuple

from pydantic import (
    SecretStr,
)
from pydantic_settings import BaseSettings


class SisuSettings(BaseSettings):
    sis_host: str
    sis_integration_user: str
    sis_integration_user_password: SecretStr = SecretStr('')
    sis_export_user: str
    sis_export_user_password: SecretStr = SecretStr('')
    socks_proxies: dict | None = None

    def get_export_auth(self) -> Tuple[str, str]:
        if not self.sis_export_user_password:
            self.sis_export_user_password = SecretStr(getpass.getpass("Give export user password: "))
        return self.sis_export_user, self.sis_export_user_password.get_secret_value()

    def get_integration_auth(self) -> Tuple[str, str]:
        if not self.sis_integration_user_password:
            self.sis_integration_user_password = SecretStr(getpass.getpass("Give integration user password: "))
        return self.sis_integration_user, self.sis_integration_user_password.get_secret_value()
