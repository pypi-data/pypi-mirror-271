from typing import Union

from bodosdk.api.base import BodoApi
from bodosdk.api.models.cloud_config import (
    AzureCloudConfigAPIModel,
    AwsCloudConfigAPIModel,
    CloudConfigAPIModel,
    CreateAwsCloudConfigAPIModel,
    CreateAzureCloudConfigAPIModel,
)
from bodosdk.interfaces import ICloudConfigApi, IAzureCloudConfig, IAwsCloudConfig


class CloudConfigApi(BodoApi, ICloudConfigApi):
    def __init__(self, *args, **kwargs):
        super(CloudConfigApi, self).__init__(*args, **kwargs)
        self._resource_url = "cloudConfig"

    def create(
        self,
        cloud_config: Union[IAwsCloudConfig, IAzureCloudConfig],
    ) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        if isinstance(cloud_config, IAwsCloudConfig):
            data = CreateAwsCloudConfigAPIModel(**cloud_config.dict())
        if isinstance(cloud_config, IAzureCloudConfig):
            data = CreateAzureCloudConfigAPIModel(**cloud_config.dict())
        resp = self._requests.post(
            self.get_resource_url(),
            data=data.json(by_alias=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def update(
        self,
        cloud_config: Union[IAwsCloudConfig, IAzureCloudConfig],
    ) -> dict:
        headers = self.get_auth_header()
        if isinstance(cloud_config, IAwsCloudConfig):
            data = AwsCloudConfigAPIModel(**cloud_config.dict())
        if isinstance(cloud_config, IAzureCloudConfig):
            data = AzureCloudConfigAPIModel(**cloud_config.dict())
        resp = self._requests.put(
            f"{self.get_resource_url()}/{cloud_config.uuid}",
            data=data.json(by_alias=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def list(self, page=None, page_size=None, order=None, provider=None, status=None):
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}",
            headers=headers,
            params={"provider": provider, "status": status},
        )
        self.handle_error(resp)
        return [CloudConfigAPIModel.parse_obj(cfg).__root__ for cfg in resp.json()]

    def get(self, uuid):
        headers = self.get_auth_header()
        resp = self._requests.get(f"{self.get_resource_url()}/{uuid}", headers=headers)
        self.handle_error(resp)
        return CloudConfigAPIModel.parse_obj(resp.json()).__root__

    def delete(self, uuid):
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/{uuid}", headers=headers
        )
        self.handle_error(resp)
