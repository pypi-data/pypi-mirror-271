from typing import Optional

from pydantic import Field

from bodosdk.base import APIBaseModel


class SnowflakeDetailsAPIModel(APIBaseModel):
    port: Optional[int]
    db_schema: Optional[str] = Field(None, alias="schema")
    database: Optional[str]
    user_role: Optional[str] = Field(None, alias="userRole")
    username: Optional[str]
    warehouse: Optional[str]
    account_name: Optional[str] = Field(None, alias="accountName")
    password: Optional[str]

    def json(self, **kwargs):
        return super().json(
            exclude={"_deprecated_fields", "_deprecated_methods"}, **kwargs
        )


class CatalogAPIModel(APIBaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    catalog_type: Optional[str] = Field(None, alias="catalogType")
    details: Optional[SnowflakeDetailsAPIModel] = Field(None, alias="data")

    def json(self, **kwargs):
        result = super().json(
            exclude={
                "_deprecated_fields": ...,
                "_deprecated_methods": ...,
                "details": {"_deprecated_fields": ..., "_deprecated_methods": ...},
            },
            **kwargs
        )
        return result
