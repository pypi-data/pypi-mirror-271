from typing import Optional

from pydantic import Field

from bodosdk.base import APIBaseModel


class SecretDefinition(APIBaseModel):
    name: Optional[str]
    data: Optional[dict]
    secret_group: Optional[str] = Field(None, alias="secretGroup")
    secret_type: Optional[str] = Field(None, alias="secretType")


class SecretInfo(APIBaseModel):
    uuid: Optional[str]
    name: Optional[str]
    secret_group: str = Field(alias="secretGroup")
    secret_type: str = Field(alias="secretType")
