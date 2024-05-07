from bodosdk.api.base import BodoApi
from bodosdk.api.models.catalog import CatalogAPIModel
from bodosdk.interfaces import ICatalog, ICatalogApi


class CatalogApi(BodoApi, ICatalogApi):
    def __init__(self, *args, **kwargs):
        super(CatalogApi, self).__init__(*args, **kwargs)
        self._resource_url = "catalogs"

    def create(self, catalog: ICatalog) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        data = CatalogAPIModel(**catalog.dict())
        resp = self._requests.post(
            self.get_resource_url("v1"),
            data=data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def get(self, uuid):
        response = self._requests.get(
            f"{self.get_resource_url('v1')}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return response.json()

    def get_by_name(self, name):
        response = self._requests.get(
            f"{self.get_resource_url('v1')}",
            headers=self.get_auth_header(),
            params={"name": name},
        )
        self.handle_error(response)
        try:
            return response.json()[0]
        except IndexError:
            return []

    def get_all(
        self,
        page=None,
        page_size=None,
        names=None,
        uuids=None,
        order=None,
    ):
        response = self._requests.get(
            f"{self.get_resource_url('v1')}",
            headers=self.get_auth_header(),
            params={"name": names, "uuid": uuids},
        )
        self.handle_error(response)
        return response.json()

    def update(self, catalog: ICatalog):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        data = CatalogAPIModel(**catalog.dict())
        response = self._requests.put(
            f"{self.get_resource_url('v1')}/{catalog.uuid}",
            data=data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(response)
        return response.json()

    def delete(self, uuid):
        response = self._requests.delete(
            f"{self.get_resource_url('v1')}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(response)

    def delete_all(self):
        response = self._requests.delete(
            f"{self.get_resource_url('v1')}", headers=self.get_auth_header()
        )
        self.handle_error(response)
