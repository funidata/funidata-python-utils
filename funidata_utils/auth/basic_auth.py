#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from pydantic import BaseModel, SecretStr


class BasicAuthUser(BaseModel):
    username: str
    password: SecretStr

    def as_tuple(self):
        return self.username, self.password.get_secret_value()
