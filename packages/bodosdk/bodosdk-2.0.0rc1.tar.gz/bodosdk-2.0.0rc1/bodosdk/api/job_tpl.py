from typing import List

from pydantic import validate_arguments

from bodosdk.api.base import BodoApi
from bodosdk.api.helpers import tags_to_query_params
from bodosdk.api.models.job import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER,
    JobTplApiModel,
)
from bodosdk.base import PaginationOrder

# helper function to compose query string from query parameters
from bodosdk.interfaces import IJobTemplate, IJobTplApi


class JobTplApi(BodoApi, IJobTplApi):
    def __init__(self, *args, **kwargs):
        super(JobTplApi, self).__init__(*args, **kwargs)
        self._resource_url = "job-templates"

    @validate_arguments
    def list_job_tpl(
        self,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
        names: List[str] = None,
        uuids: List[str] = None,
        tags: dict = None,
    ) -> dict:
        headers = self.get_auth_header()
        resource_url = f"{self.get_resource_url('v1')}"
        resp = self._requests.get(
            resource_url,
            headers=headers,
            params={
                "page": page,
                "size": size,
                "order": order,
                "name": names,
                "uuid": uuids,
                "tag": tags_to_query_params(tags),
            },
        )
        self.handle_error(resp)
        return resp.json()

    def delete_job_tpl(self, uuid):
        headers = self.get_auth_header()
        resource_url = f"{self.get_resource_url('v1')}/{uuid}"
        resp = self._requests.delete(
            resource_url,
            headers=headers,
        )
        self.handle_error(resp)

    def create_job_tpl(self, tpl: IJobTemplate):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        tpl_dict = tpl.dict(by_alias=True)
        tpl_dict["config"]["source"] = {
            "type": tpl.config.source.type,
            "sourceDef": tpl.config.source,
        }
        request_data = JobTplApiModel(**tpl_dict)
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}",
            data=request_data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def get_job_tpl(self, uuid):
        headers = self.get_auth_header()
        resource_url = f"{self.get_resource_url('v1')}/{uuid}"
        resp = self._requests.get(
            resource_url,
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def update_job_tpl(self, tpl: IJobTemplate):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        tpl_dict = tpl.dict(by_alias=True)
        tpl_dict["config"]["source"] = {
            "type": tpl.config.source.type,
            "sourceDef": tpl.config.source,
        }
        request_data = JobTplApiModel(**tpl.dict())
        resp = self._requests.patch(
            f"{self.get_resource_url('v1')}/{tpl.uuid}",
            data=request_data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()
