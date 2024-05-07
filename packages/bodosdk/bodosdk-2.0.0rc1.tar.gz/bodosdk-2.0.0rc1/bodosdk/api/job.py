import logging
from datetime import datetime
from typing import List, Union
from uuid import UUID

from pydantic import validate_arguments

from bodosdk.api.base import BodoApi
from bodosdk.api.models.job import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER,
    JobRunApiModel,
)
from bodosdk.base import PaginationOrder
from bodosdk.api.models.job import (
    JobRunLogsResponseApiModel,
)

# helper function to compose query string from query parameters
from bodosdk.interfaces import IJobRun, IJobApi


class JobApi(BodoApi, IJobApi):
    def __init__(self, *args, **kwargs):
        super(JobApi, self).__init__(*args, **kwargs)
        self._resource_url = "jobs"

    @validate_arguments
    def list_job_runs(
        self,
        uuids: List[str] = None,
        types: List[str] = None,
        template_ids: Union[List[UUID], None] = None,
        statuses: Union[List[str], None] = None,
        cluster_ids: Union[List[UUID], None] = None,
        started_at: Union[datetime, None] = None,
        finished_at: Union[datetime, None] = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
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
                "uuid": uuids,
                "type": types,
                "jobTemplateUUID": template_ids,
                "clusterUUID": cluster_ids,
                "status": statuses,
                "startedAt": started_at,
                "finishedAt": finished_at,
            },
        )
        self.handle_error(resp)
        return resp.json()

    def get_job_log_links(self, uuid, force_refresh) -> JobRunLogsResponseApiModel:
        try:
            headers = self.get_auth_header()
            url = f"{self.get_resource_url('v1')}/{uuid}/logs?forceRefresh={str(force_refresh).lower()}"
            resp = self._requests.get(url, headers=headers)
            self.handle_error(resp)
            json_data = resp.json()
            job_run_logs_response = JobRunLogsResponseApiModel(**json_data)

            def fetch_and_write_file(url: str, file_name: str) -> None:
                try:
                    response = self._requests.get(url)
                    if response.status_code == 200:
                        with open(file_name, "wb") as file:
                            file.write(response.content)
                    else:
                        logging.error(
                            f"File {file_name} fetch failed: {response.status_code}"
                        )
                except Exception as e:
                    logging.error(f"Bad File fetch Response: {e}")

            fetch_and_write_file(
                job_run_logs_response.stdout_location_url, f"stdout_{uuid}.txt"
            )
            fetch_and_write_file(
                job_run_logs_response.stderr_location_url, f"stderr_{uuid}.txt"
            )
            return job_run_logs_response
        except Exception as e:
            logging.error(f"Bad Response: {e}")

    def create_job_run(self, job_run: IJobRun):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        job_run_dict = job_run.dict(by_alias=True)
        if job_run_dict.get("config", {}).get("source"):
            job_run_dict["config"]["source"] = {
                "type": job_run.config.source.type,
                "sourceDef": job_run.config.source,
            }
        request_data = JobRunApiModel(**job_run_dict)
        resp = self._requests.post(
            f"{self.get_resource_url('v1')}",
            data=request_data.json(by_alias=True, exclude_none=True),
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def get_job(self, uuid) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.get(
            f"{self.get_resource_url('v1')}/{uuid}",
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()

    def cancel_job(self, uuid) -> dict:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.delete(
            f"{self.get_resource_url('v1')}/{uuid}",
            headers=headers,
        )
        self.handle_error(resp)
        return resp.json()
