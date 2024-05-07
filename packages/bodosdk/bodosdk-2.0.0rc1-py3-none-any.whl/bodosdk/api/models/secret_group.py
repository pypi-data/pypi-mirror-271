from typing import Optional

from bodosdk.base import APIBaseModel


class SecretGroupDefinition(APIBaseModel):
    name: str
    description: Optional[str]


class SecretGroupInfo(APIBaseModel):
    uuid: str
    name: str
    description: str
