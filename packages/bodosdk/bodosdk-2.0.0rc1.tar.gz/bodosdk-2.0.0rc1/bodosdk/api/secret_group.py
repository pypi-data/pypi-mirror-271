from typing import List

from bodosdk.api.base import BodoApi
from bodosdk.api.models.secret_group import SecretGroupDefinition
from bodosdk.interfaces import ISecretGroup, ISecretGroupApi


class SecretGroupApi(BodoApi, ISecretGroupApi):
    def __init__(self, *args, **kwargs):
        super(SecretGroupApi, self).__init__(*args, **kwargs)
        self._resource_url = "secret-group"

    def create_secret_group(self, secret_group: ISecretGroup) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        data = SecretGroupDefinition(**secret_group.dict())
        resp = self._requests.post(
            self.get_resource_url(),
            data=data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def get_secret_groups(
        self, page=None, page_size=None, names=None, order=None
    ) -> List[dict]:
        response = self._requests.get(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return response.json()

    def update_secret_group(self, secret_group: ISecretGroup) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())

        data = SecretGroupDefinition(**secret_group.dict())

        response = self._requests.put(
            f"{self.get_resource_url()}/{data.name}",
            data=data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )

        self.handle_error(response)
        return response.json()

    def delete_secret_group(self, name: str):
        response = self._requests.delete(
            f"{self.get_resource_url()}/{name}",
            headers=self.get_auth_header(),
        )
        self.handle_error(response)
