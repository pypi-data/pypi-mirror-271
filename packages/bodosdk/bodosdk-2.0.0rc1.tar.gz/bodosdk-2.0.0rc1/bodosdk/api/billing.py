from datetime import date
from typing import Union
from uuid import UUID

from pydantic import validate_arguments

from bodosdk.api.base import BodoApi
from bodosdk.base import PaginationOrder
from bodosdk.api.models.cluster import (
    ClusterPriceExportResponse,
    ClusterPricingResponse,
)
from bodosdk.api.models.job import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER,
)
from bodosdk.api.models.job import JobRunPriceExportResponse, JobRunPricingResponse


class BillingApi(BodoApi):
    def __init__(self, *args, **kwargs):
        super(BillingApi, self).__init__(*args, **kwargs)

    @validate_arguments
    def get_cluster_prices(
        self,
        started_at: Union[str, date],
        finished_at: Union[str, date],
        workspace_uuid: Union[str, UUID] = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())

        url = f"{self.get_resource_url()}/metering/pricing?startedAt={started_at}"
        f"&finishedAt={finished_at}&page={page}&size={size}&order={order.value}"

        if workspace_uuid is not None:
            url = f"{url}&workspaceUUID={workspace_uuid}"

        resp = self._requests.get(url, headers=headers)
        self.handle_error(resp)
        return ClusterPricingResponse(**resp.json())

    @validate_arguments
    def get_job_run_prices(
        self,
        started_at: Union[str, date],
        finished_at: Union[str, date],
        workspace_uuid: Union[str, UUID] = None,
        page: int = DEFAULT_PAGE,
        size: int = DEFAULT_PAGE_SIZE,
        order: PaginationOrder = DEFAULT_ORDER,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())

        url = f"{self.get_resource_url()}/v1/jobs/pricing?startedAt={started_at}"
        f"&finishedAt={finished_at}&page={page}&size={size}&order={order.value}"

        if workspace_uuid is not None:
            url = f"{url}&workspaceUUID={workspace_uuid}"

        resp = self._requests.get(url, headers=headers)
        self.handle_error(resp)
        return JobRunPricingResponse(**resp.json())

    @validate_arguments
    def get_cluster_price_export(
        self,
        started_at: Union[str, date],
        finished_at: Union[str, date],
        workspace_uuid: Union[str, UUID] = None,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        url = f"{self.get_resource_url()}/metering/price-export?startedAt={started_at}&finishedAt={finished_at}"

        if workspace_uuid is not None:
            url = f"{url}&workspaceUUID={workspace_uuid}"

        resp = self._requests.get(url, headers=headers)
        self.handle_error(resp)
        return ClusterPriceExportResponse(**resp.json())

    @validate_arguments
    def get_job_run_price_export(
        self,
        started_at: Union[str, date],
        finished_at: Union[str, date],
        workspace_uuid: Union[str, UUID] = None,
    ):
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())

        url = f"{self.get_resource_url()}/v1/jobs/price-export?startedAt={started_at}&finishedAt={finished_at}"

        if workspace_uuid is not None:
            url = f"{url}&workspaceUUID={workspace_uuid}"

        resp = self._requests.get(url, headers=headers)
        self.handle_error(resp)
        return JobRunPriceExportResponse(**resp.json())
