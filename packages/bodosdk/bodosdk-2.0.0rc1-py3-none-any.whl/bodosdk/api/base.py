from typing import Optional

import bodosdk
from bodosdk.api.auth import AuthApi
from bodosdk.api.request_wrapper import RequestWrapper
from bodosdk.base import APIBaseModel
from bodosdk.exceptions import (
    ValidationError,
    ServiceUnavailable,
    ResourceNotFound,
    ConflictException,
)


class BodoApi:
    def __init__(
        self,
        auth_api: AuthApi,
        api_url="https://api.bodo.ai/api",
        requests=RequestWrapper(),
    ):
        self._requests = requests
        self._auth_api = auth_api
        self._base_url = api_url
        self._resource_url = ""

    def get_auth_header(self):
        token = self._auth_api.auth_token
        return {
            "Authorization": f"Bearer {token}",
            "SDK-Version": bodosdk._version.get_versions().get("version"),
        }

    def get_resource_url(self, version=None):
        if not self._resource_url:
            return f"{self._base_url}/{version}" if version else self._base_url

        return (
            f"{self._base_url}/{version}/{self._resource_url}"
            if version
            else f"{self._base_url}/{self._resource_url}"
        )

    def handle_error(self, response):
        try:
            msg = response.json()
        except Exception:
            msg = response.content
        if response.status_code in (400, 422):
            raise ValidationError(msg)
        if response.status_code in (500, 503):
            raise ServiceUnavailable
        if response.status_code == 404:
            raise ResourceNotFound(msg)
        if response.status_code == 409:
            raise ConflictException(msg)
        response.raise_for_status()


class PageMetadata(APIBaseModel):
    page: int
    size: int
    order: Optional[str]
    total_pages: int
    total_items: int
