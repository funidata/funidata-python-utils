#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from pydantic import BaseModel, SecretStr


class AwsAccesKeyConfig(BaseModel):
    endpoint_url: str | None
    aws_access_key_id: str | None
    aws_secret_access_key: SecretStr
    region_name: str | None


class AwsProfileConfig(AwsAccesKeyConfig):
    aws_profile: str


class EmptyAwsConfig(BaseModel):
    ...

    class Config:
        extra = "forbid"


class AwsConfig(BaseModel):
    s3: AwsProfileConfig | AwsAccesKeyConfig | EmptyAwsConfig
