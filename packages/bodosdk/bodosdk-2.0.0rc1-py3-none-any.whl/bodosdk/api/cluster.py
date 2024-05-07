import datetime
from typing import Dict, Optional, List, Union

from bodosdk.api.base import BodoApi
from bodosdk.api.helpers import ordering_to_query_params, tags_to_query_params
from bodosdk.base import PaginationOrder
from bodosdk.api.models.cluster import (
    ClusterDefinition,
    ClusterResponse,
    ModifyCluster,
    ClusterListAPIModel,
)


class ClusterApi(BodoApi):
    def __init__(self, *args, **kwargs):
        super(ClusterApi, self).__init__(*args, **kwargs)
        self._resource_url = "clusters"

    def get_cluster(self, uuid) -> ClusterResponse:
        response = self._requests.get(
            f"{self.get_resource_url('v1')}/{uuid}", headers=self.get_auth_header()
        )
        self.handle_error(response)
        return ClusterResponse(**response.json())

    def get_all_clusters(
        self,
        page: int = 1,
        page_size: int = 10,
        order: str = PaginationOrder.ASC.value,
        cluster_names: Optional[List[str]] = None,
        uuids: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
        ordering: Optional[Dict] = None,
        created_on: Optional[Union[datetime.date, str]] = None,
        tags: Optional[Dict] = None,
    ) -> ClusterListAPIModel:
        response = self._requests.get(
            f"{self.get_resource_url('v2')}",
            headers=self.get_auth_header(),
            params={
                "page": page,
                "size": page_size,
                "order": order,
                "clusterName": cluster_names,
                "status": statuses,
                "uuid": uuids,
                "createdOn": created_on,
                "ordering": ordering_to_query_params(ordering),
                "tag": tags_to_query_params(tags),
            },
        )
        self.handle_error(response)
        return ClusterListAPIModel(**response.json())

    def create_cluster(self, cluster_definition: ClusterDefinition) -> ClusterResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}",
            data=cluster_definition.json(by_alias=True),
            headers=headers,
        )
        self.handle_error(resp)
        return ClusterResponse(**resp.json())

    def remove_cluster(self, uuid, force_remove, mark_as_terminated):
        params = {
            "force": str(force_remove).lower(),
            "mark_as_terminated": str(mark_as_terminated).lower(),
        }
        response = self._requests.delete(
            f"{self.get_resource_url('v1')}/{uuid}",
            params=params,
            headers=self.get_auth_header(),
        )
        self.handle_error(response)
        return ClusterResponse(**response.json())

    def modify_cluster(self, modify_cluster: ModifyCluster):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.patch(
            f"{self.get_resource_url('v1')}/{modify_cluster.uuid}",
            data=modify_cluster.json(
                by_alias=True, exclude={"uuid": True}, exclude_none=True
            ),
            headers=headers,
        )
        self.handle_error(resp)
        return ClusterResponse(**resp.json())

    def pause(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.put(
            f"{self.get_resource_url('v1')}/{uuid}/pause", headers=headers
        )
        self.handle_error(resp)
        return ClusterResponse(**resp.json())

    def resume(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.put(
            f"{self.get_resource_url('v1')}/{uuid}/resume", headers=headers
        )
        self.handle_error(resp)
        return ClusterResponse(**resp.json())

    def stop(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}/{uuid}/stop", headers=headers
        )
        self.handle_error(resp)
        return ClusterResponse(**resp.json())

    def restart(self, uuid):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}/{uuid}/restart", headers=headers
        )
        self.handle_error(resp)
        return ClusterResponse(**resp.json())
