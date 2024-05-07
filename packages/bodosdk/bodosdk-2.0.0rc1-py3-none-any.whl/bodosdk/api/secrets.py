from bodosdk.api.base import BodoApi
from bodosdk.api.models.secrets import SecretDefinition, SecretInfo
from bodosdk.interfaces import ISecret, ISecretsApi


class SecretsApi(BodoApi, ISecretsApi):
    def __init__(self, *args, **kwargs):
        super(SecretsApi, self).__init__(*args, **kwargs)
        self._resource_url = "secrets"

    def create_secret(self, secret: ISecret) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        data = SecretDefinition(**secret.dict())
        resp = self._requests.post(
            self.get_resource_url(),
            data=data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def get_secret(self, uuid) -> dict:
        response = self._requests.get(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return response.json()

    def get_all_secrets(
        self, page=None, page_size=None, names=None, secret_groups=None, order=None
    ):
        response = self._requests.get(
            f"{self.get_resource_url()}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return response.json()

    def get_all_secrets_by_group(self, secret_group: str):
        response = self._requests.get(
            f"{self.get_resource_url()}/secret-group/{secret_group}",
            headers=self.get_auth_header(),
        )
        self.handle_error(response)
        return [SecretInfo(**s) for s in response.json()]

    def update_secret(self, secret: ISecret) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        data = SecretDefinition(**secret.dict())
        response = self._requests.put(
            f"{self.get_resource_url()}/{secret.uuid}",
            data=data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(response)
        return response.json()

    def delete_secret(self, uuid):
        response = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(response)
