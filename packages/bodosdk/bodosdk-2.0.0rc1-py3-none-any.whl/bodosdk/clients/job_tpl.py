from typing import Dict, Union

from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.interfaces import (
    IBodoWorkspaceClient,
    IGitRepoSource,
    IS3Source,
    IWorkspaceSource,
    ICluster,
    IJobTemplateClient,
    ITextSource,
)
from bodosdk.models import JobTemplateList, JobTemplate


class JobTemplateClient(IJobTemplateClient):
    _deprecated_methods: Dict = {}

    def __init__(self, workspace_client: IBodoWorkspaceClient):
        self._workspace_client = workspace_client
        self._check_deprecation()

    def _check_deprecation(self):
        methods = self._workspace_client._sdk_api.get_job_tpl_client_info()
        if isinstance(methods, dict) and methods:
            self._deprecated_methods = methods

    @property
    def JobTemplate(self) -> JobTemplate:
        return JobTemplate(workspace_client=self._workspace_client)

    @property
    def JobTemplateList(self) -> JobTemplateList:
        return JobTemplateList(workspace_client=self._workspace_client)

    @check_deprecation
    def create(
        self,
        name: str = None,
        description: str = None,
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
        catalog: str = None,
    ) -> JobTemplate:
        if isinstance(cluster, dict):
            cluster = self._workspace_client.ClusterClient.Cluster(**cluster)
        data = {
            "name": name,
            "description": description,
            "config": {
                "type": code_type,
                "source": {"type": "SQL"}
                if code_type == "SQL" and exec_text
                else source,
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
        data["cluster_config"] = cluster
        return self.JobTemplate(**data)._save()

    @check_deprecation
    def get(self, id: str) -> JobTemplate:
        return self.JobTemplate(uuid=id)._load()

    @check_deprecation
    def remove(self, id: str):
        return self.JobTemplate(uuid=id).delete()

    @check_deprecation
    def list(self, filters: Dict = None) -> JobTemplateList:
        return self.JobTemplateList(filters=filters)
