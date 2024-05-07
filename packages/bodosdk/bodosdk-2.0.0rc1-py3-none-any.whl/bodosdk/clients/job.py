from typing import Dict, List, Optional, Union

import bodosdk.models.job
from bodosdk import _version
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.interfaces import (
    IJobClient,
    IBodoWorkspaceClient,
    IS3Source,
    IGitRepoSource,
    IWorkspaceSource,
    ITextSource,
    ICluster,
)
from bodosdk.models.job import TextSource, JobFilter


class JobClient(IJobClient):
    _deprecated_methods: Dict

    def __init__(self, workspace_client: IBodoWorkspaceClient):
        self._workspace_client = workspace_client
        self._check_deprecation()

    def _check_deprecation(self):
        methods = self._workspace_client._sdk_api.get_job_client_info(
            _version.get_versions().get("version")
        )
        if isinstance(methods, dict) and methods:
            self._deprecated_methods = methods
        else:
            self._deprecated_methods = {}

    @property
    def JobRun(self) -> bodosdk.models.job.JobRun:
        return bodosdk.models.job.JobRun(self._workspace_client)

    @property
    def JobRunList(self) -> bodosdk.models.job.JobRunList:
        return bodosdk.models.job.JobRunList(self._workspace_client)

    @check_deprecation
    def run(
        self,
        template_id: str = None,
        cluster: Union[dict, ICluster] = None,
        code_type: str = None,
        source: Union[
            dict, IS3Source, IGitRepoSource, IWorkspaceSource, ITextSource
        ] = None,
        exec_file: str = None,
        exec_text: str = None,
        args: Union[dict, str] = None,
        env_vars: dict = None,
        timeout: int = None,
        num_retries: int = None,
        delay_between_retries: int = None,
        retry_on_timeout: bool = None,
        name: str = None,
        catalog: str = None,
    ) -> bodosdk.models.job.JobRun:
        if isinstance(cluster, dict):
            cluster = self._workspace_client.ClusterClient.Cluster(**cluster)
        data = {
            "name": name,
            "job_template_id": template_id,
            "config": {
                "type": code_type,
                "source": source,
                "exec_file": exec_file,
                "exec_text": exec_text,
                "args": args if code_type != "SQL" else None,
                "sql_query_parameters": args if code_type == "SQL" else None,
                "env_vars": env_vars,
                "timeout": timeout,
                "catalog": catalog,
            },
        }
        if (
            num_retries is not None
            or delay_between_retries is not None
            or retry_on_timeout is not None
        ):
            data["config"]["retry_strategy"] = {
                "num_retries": num_retries,
                "delay_between_retries": delay_between_retries,
                "retry_on_timeout": retry_on_timeout,
            }
        if cluster and cluster.id:
            data["cluster_id"] = cluster.id
        else:
            data["cluster_config"] = cluster
        job = self.JobRun(**data)
        return job._save()

    @check_deprecation
    def run_sql_query(
        self,
        template_id: str = None,
        catalog: str = None,
        sql_query: str = None,
        cluster: Union[dict, ICluster] = None,
        name: str = None,
        args: dict = None,
        timeout: int = None,
        num_retries: int = None,
        delay_between_retries: int = None,
        retry_on_timeout: bool = None,
    ) -> bodosdk.models.job.JobRun:
        if isinstance(cluster, dict):
            cluster = self._workspace_client.ClusterClient.Cluster(**cluster)
        data = {
            "name": name,
            "job_template_id": template_id,
            "config": {
                "type": "SQL",
                "source": TextSource(),
                "exec_text": sql_query,
                "catalog": catalog,
                "sql_query_parameters": args,
                "timeout": timeout,
            },
        }
        if (
            num_retries is not None
            or delay_between_retries is not None
            or retry_on_timeout is not None
        ):
            data["retry_strategy"] = {
                "num_retries": num_retries,
                "delay_between_retries": delay_between_retries,
                "retry_on_timeout": retry_on_timeout,
            }
        if cluster and cluster.id:
            data["cluster_id"] = cluster.id
        else:
            data["cluster_config"] = cluster
        job = self.JobRun(**data)
        return job._save()

    @check_deprecation
    def get(self, id: str) -> bodosdk.models.job.JobRun:
        return self.JobRun(uuid=id)._load()

    @check_deprecation
    def list(
        self,
        filters: Optional[Union[Dict, JobFilter]] = None,
        order: Optional[Dict] = None,
    ) -> bodosdk.models.job.JobRunList:
        return self.JobRunList(filters=filters, order=order)

    @check_deprecation
    def cancel_job(self, id: str) -> bodosdk.models.job.JobRun:
        return self.JobRun(uuid=id).cancel()

    @check_deprecation
    def cancel_jobs(
        self, filters: Optional[Union[Dict, JobFilter]] = None
    ) -> bodosdk.models.job.JobRunList:
        return self.JobRunList(filters=filters).cancel()

    @check_deprecation
    def wait_for_status(
        self, id: str, statuses: List[str], timeout: int = 3600, tick: int = 30
    ) -> bodosdk.models.job.JobRun:
        return self.JobRun(uuid=id).wait_for_status(
            statuses=statuses, timeout=timeout, tick=tick
        )
