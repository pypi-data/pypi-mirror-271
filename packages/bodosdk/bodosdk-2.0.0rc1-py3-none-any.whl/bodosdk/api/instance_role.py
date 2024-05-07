from typing import List

from bodosdk.api.base import BodoApi
from bodosdk.api.helpers import ordering_to_query_params
from bodosdk.api.models.instance_role import (
    InstanceRoleListAPIModel,
    InstanceRoleApiModel,
)


class InstanceRoleApi(BodoApi):
    def __init__(self, *args, **kwargs):
        super(InstanceRoleApi, self).__init__(*args, **kwargs)
        self._resource_url = "instance-roles"

    def get_role(self, uuid) -> InstanceRoleApiModel:
        response = self._requests.get(
            f"{self.get_resource_url('v1')}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return InstanceRoleApiModel(**response.json())

    def get_all_roles(self) -> List[InstanceRoleApiModel]:
        response = self._requests.get(
            f"{self.get_resource_url('v1')}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return [InstanceRoleApiModel(**ir) for ir in response.json()]

    def create_role(
        self, role_definition: InstanceRoleApiModel
    ) -> InstanceRoleApiModel:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url("v1"), data=role_definition.json(), headers=headers
        )
        self.handle_error(resp)
        return InstanceRoleApiModel(**resp.json())

    def remove_role(self, uuid, mark_as_terminated):
        params = {"mark_as_terminated": str(mark_as_terminated).lower()}
        response = self._requests.delete(
            f"{self.get_resource_url('v1')}/{uuid}",
            params=params,
            headers=self.get_auth_header(),
        )
        self.handle_error(response)

    def list(
        self,
        page=1,
        page_size=10,
        role_names=None,
        uuids=None,
        role_arns=None,
        order=None,
    ):
        response = self._requests.get(
            f"{self.get_resource_url('v1')}",
            headers=self.get_auth_header(),
            params={
                "page": page,
                "size": page_size,
                "name": role_names,
                "roleArn": role_arns,
                "uuid": uuids,
                "ordering": ordering_to_query_params(order),
            },
        )
        self.handle_error(response)
        return InstanceRoleListAPIModel(**response.json())
