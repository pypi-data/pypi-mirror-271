from typing import Union, List, Optional
from uuid import UUID

from bodosdk.api.base import BodoApi
from bodosdk.api.models.workspace import (
    UserAssignment,
    WorkspaceAPIModel,
    WorkspaceListAPIModel,
)
from bodosdk.interfaces import IWorkspaceApi, IWorkspace
from bodosdk.models.cluster import InstanceType, BodoImage


class WorkspaceApi(BodoApi, IWorkspaceApi):
    def __init__(self, *args, **kwargs):
        super(WorkspaceApi, self).__init__(*args, **kwargs)
        self._resource_url = "workspaces"

    def create(self, workspace_definition: WorkspaceAPIModel):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}",
            data=workspace_definition.json(by_alias=True),
            headers=headers,
        )
        self.handle_error(resp)
        return WorkspaceAPIModel(**resp.json())

    def get(self, uuid) -> WorkspaceAPIModel:
        resp = self._requests.get(
            f"{self.get_resource_url('v1')}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(resp)
        return WorkspaceAPIModel(**resp.json())

    def list(
        self,
        page: int = 1,
        page_size: int = 10,
        names: Optional[List[str]] = None,
        uuids: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ):
        response = self._requests.get(
            f"{self.get_resource_url('v1')}",
            headers=self.get_auth_header(),
            params={
                "page": page,
                "size": page_size,
                "status": statuses,
                "name": names,
                "uuid": uuids,
            },
        )
        self.handle_error(response)
        return WorkspaceListAPIModel(**response.json())

    def remove(self, uuid, mark_as_terminated=False):
        params = {"mark_as_terminated": str(mark_as_terminated).lower()}
        response = self._requests.delete(
            f"{self.get_resource_url('v1')}/{uuid}",
            params=params,
            headers=self.get_auth_header(),
        )
        self.handle_error(response)
        return WorkspaceAPIModel(**response.json())

    def assign_users(self, uuid: Union[str, UUID], users: List[UserAssignment]):
        response = self._requests.post(
            f"{self.get_resource_url('v1')}/{str(uuid)}/users",
            json={"users": [u.dict(by_alias=True) for u in users]},
            headers=self.get_auth_header(),
        )
        self.handle_error(response)

    def available_instances(self, uuid) -> List[InstanceType]:
        resp = self._requests.get(
            f"{self.get_resource_url('v1')}/{str(uuid)}/available-instances",
            headers=self.get_auth_header(),
        )
        self.handle_error(resp)
        result = []
        for row in resp.json():
            for opt in row.get("options", []):
                result.append(InstanceType(**opt["label"]))
        return result

    def available_images(self, uuid) -> List[BodoImage]:
        resp = self._requests.get(
            f"{self.get_resource_url('v1')}/{str(uuid)}/available-images",
            headers=self.get_auth_header(),
        )
        self.handle_error(resp)
        result = []
        for row in resp.json():
            for opt in row.get("options"):
                img = BodoImage(
                    image_id=opt["label"]["imageId"],
                    bodo_version=opt["label"]["bodo_version"],
                )
                result.append(img)
        return result

    def update_infra(self, workspace: IWorkspace):
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}/{str(workspace.id)}/update-infrastructure",
            headers=self.get_auth_header(),
        )
        self.handle_error(resp)
