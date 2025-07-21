#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from typing import ClassVar

from .basic_auth import BasicAuthUser
from .source_config import SourceConfig


class SisuConfig(SourceConfig):
    name: ClassVar[str] = 'sisu'
    root_organisation: str
    integration_user: BasicAuthUser
    export_user: BasicAuthUser

    def get_export_auth(self) -> tuple[str, str]:
        return self.export_user.as_tuple()

    def get_integration_auth(self) -> tuple[str, str]:
        return self.integration_user.as_tuple()
