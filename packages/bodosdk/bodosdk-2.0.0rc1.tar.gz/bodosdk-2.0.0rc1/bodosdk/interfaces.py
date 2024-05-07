from __future__ import annotations
from abc import abstractmethod, ABC
from collections.abc import Iterable
from datetime import datetime
from typing import Dict, Optional, Union, List, Sized, Any
from unittest.mock import MagicMock
from uuid import UUID

from bodosdk.api.auth import AuthApi
from bodosdk.api.cluster import ClusterApi
from bodosdk.api.instance_role import InstanceRoleApi


class IBaseList(ABC, Iterable, Sized):
    page: Optional[int]
    page_size: Optional[int]
    total: Optional[int]
    order: Optional[Dict]
    filters: Optional[Dict]
    _elements: List
    _index: int

    @abstractmethod
    def __call__(self, **data) -> Any:
        raise NotImplementedError

    def __iter__(self) -> Any:
        """
        Provides an iterator over the elements in the list. It supports iteration
        through the elements, automatically loading the next page of elements when
        necessary.

        Returns:
            Iterator[Any]: An iterator over the elements in the list.
        """
        self._index = 0
        for element in self._elements:
            yield element
            self._index += 1
            if self._index == len(self._elements) and self.total > self._index:
                self._load_next_page()

    def __len__(self) -> int:
        """
        Returns the total number of element available across all pages, according
        to the last known state from the workspace API.

        Returns:
            int: The total number of element available.
        """
        return self.total

    def __getitem__(self, key) -> Union[Any, List[Any]]:
        """
        Supports accessing individual element or a slice of element from the list,
        handling pagination transparently. This method enables indexing and slicing
        operations.

        Args:
            key (int | slice): The index or slice indicating which element to access.

        Returns:
            Union[Any, List[Any]]: A single element or a list of element, depending
                on the type of key provided.

        Raises:
            IndexError: If the key is out of the bounds of the cluster list.
        """
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or self.total - 1
            max_index = max(
                max(start, self.total + start if start < 0 else 0),
                max(stop, self.total + stop if stop < 0 else 0),
            )
            while min(max_index, self.total - 1) >= len(self._elements):
                self._load_next_page()
            return self._elements[key.start : key.stop : key.step]  # noqa
        if key > self.total - 1 or key < self.total * -1:
            raise IndexError
        elif key < 0:
            index = self.total + key
        else:
            index = key
        while index >= len(self._elements):
            self._load_next_page()
        return self._elements[index]

    def __contains__(self, obj) -> bool:
        """
        Checks if a specific element is present in the current list of element.

        Args:
            obj: The element object to check for presence in the list.

        Returns:
            bool: True if the element is present in the list; False otherwise.
        """
        return obj in self._elements

    @abstractmethod
    def _load_next_page(self) -> Any:
        raise NotImplementedError


class IWorkspaceApi(ABC):
    @abstractmethod
    def create(self, workspace_definition):
        raise NotImplementedError

    @abstractmethod
    def get(self, uuid):
        raise NotImplementedError

    @abstractmethod
    def remove(self, uuid, mark_as_terminated=False):
        raise NotImplementedError

    @abstractmethod
    def assign_users(self, uuid, users):
        raise NotImplementedError

    @abstractmethod
    def available_instances(self, uuid):
        raise NotImplementedError

    @abstractmethod
    def available_images(self, uuid) -> List["IBodoImage"]:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        page: int,
        page_size: int,
        uuids: Optional[List[str]],
        statuses: Optional[List[str]],
        names: Optional[List[str]],
    ) -> IWorkspaceList:
        raise NotImplementedError

    @abstractmethod
    def update_infra(self, workspace: IWorkspace):
        raise NotImplementedError


class IBodoImage(ABC):
    image_id: str
    bodo_version: str


class IWorkspaceFilter:
    ids: Optional[List[str]]
    names: Optional[List[str]]
    statuses: Optional[List[str]]


class IWorkspaceList(IBaseList):
    @abstractmethod
    def __call__(self, **data) -> "IWorkspaceList":
        raise NotImplementedError

    @abstractmethod
    def delete(self, wait=False) -> "IWorkspaceList":
        raise NotImplementedError

    @abstractmethod
    def update_infra(self) -> "IWorkspaceList":
        raise NotImplementedError


class IInstanceRoleFilter:
    names: List[str]
    ids: List[str]
    role_arns: List[str]


class IInstanceRoleClient:
    InstanceRole: "IInstanceRole"
    InstanceRoleList: "IInstanceRoleList"

    @abstractmethod
    def list(
        self, filters: Optional[Union[dict, IInstanceRoleFilter]], order: dict
    ) -> "IInstanceRoleList":
        raise NotImplementedError

    @abstractmethod
    def get(self, id) -> "IInstanceRole":
        raise NotImplementedError

    @abstractmethod
    def create(self, role_arn, name=None, description=None) -> "IInstanceRole":
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError


class IJobApi(ABC):
    @abstractmethod
    def get_job_log_links(self, uuid, force_refresh):
        raise NotImplementedError

    @abstractmethod
    def create_job_run(self, job_run: IJobRun) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_job(self, uuid) -> dict:
        raise NotImplementedError

    @abstractmethod
    def cancel_job(self, uuid) -> dict:
        raise NotImplementedError

    def list_job_runs(
        self,
        uuids: List[str] = None,
        types: List[str] = None,
        template_ids: Union[List[UUID], None] = None,
        statuses: Union[List[str], None] = None,
        cluster_ids: Union[List[UUID], None] = None,
        started_at: Union[datetime, None] = None,
        finished_at: Union[datetime, None] = None,
        page: int = None,
        size: int = None,
        order: str = None,
    ) -> dict:
        raise NotImplementedError


class IJobTplApi(ABC):
    @abstractmethod
    def list_job_tpl(
        self,
        page: int = None,
        size: int = None,
        order: str = None,
        names: List[str] = None,
        uuids: List[str] = None,
        tags: dict = None,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    def delete_job_tpl(self, uuid):
        raise NotImplementedError

    @abstractmethod
    def create_job_tpl(self, tpl: IJobTemplate):
        raise NotImplementedError

    @abstractmethod
    def update_job_tpl(self, tpl: IJobTemplate):
        raise NotImplementedError

    @abstractmethod
    def get_job_tpl(self, uuid):
        raise NotImplementedError


class IBodoWorkspaceClient(ABC):
    _workspace_uuid: str
    _client_id: str
    _secret_key: str

    ClusterClient: "IClusterClient"
    JobClient: "IJobClient"
    JobTemplateClient: "IJobTemplateClient"
    InstanceRoleClient: IInstanceRoleClient
    CatalogClient: ICatalogClient

    # Private fields
    _api_url: str
    _auth_url: str
    _sdk_api: MagicMock
    _job_api: IJobApi
    _job_tpl_api: IJobTplApi
    _auth_api: AuthApi
    _cluster_api: ClusterApi
    _instance_api: InstanceRoleApi
    _secrets_api: ISecretsApi
    _secret_group_api: ISecretGroupApi
    _catalog_api: ICatalogApi
    _workspace_api: IWorkspaceApi

    _print_logs: bool
    _deprecated_methods: Dict

    @property
    def Cluster(self) -> ICluster:
        raise NotImplementedError

    @property
    def ClusterList(self) -> IClusterList:
        raise NotImplementedError


class IBodoOrganizationClient:
    _client_id: str
    _secret_key: str

    _api_url: str
    _auth_url: str
    _sdk_api: MagicMock
    _auth_api: AuthApi
    _workspace_api: IWorkspaceApi
    _cloud_config_api: ICloudConfigApi

    _print_logs: bool
    _deprecated_methods: Dict

    @property
    def Workspace(self) -> IWorkspace:
        raise NotImplementedError

    @property
    def WorkspaceList(self) -> IWorkspaceList:
        raise NotImplementedError

    @property
    def CloudConfig(self) -> ICloudConfig:
        raise NotImplementedError

    @property
    def AwsCloudConfig(self) -> ICloudConfig:
        raise NotImplementedError

    @property
    def AzureCloudConfig(self) -> ICloudConfig:
        raise NotImplementedError

    @property
    def CloudConfigList(self) -> ICloudConfigList:
        raise NotImplementedError

    @abstractmethod
    def create_workspace(
        self,
        name: str,
        region: str,
        storage_endpoint_enabled: bool,
        cloud_config_id: str = None,
        vpc_id: Optional[str] = None,
        public_subnets_ids: Optional[List[str]] = None,
        private_subnets_ids: Optional[List[str]] = None,
        custom_tags: Optional[dict] = None,
    ) -> IWorkspace:
        raise NotImplementedError

    @abstractmethod
    def delete_workspace(self, id) -> IWorkspace:
        raise NotImplementedError


class IAwsProviderData:
    role_arn: Optional[str]
    tf_bucket_name: Optional[str]
    tf_dynamo_db_table_name: Optional[str]
    tf_backend_region: Optional[str]
    external_id: Optional[str]
    account_id: Optional[str]


class IAzureProviderData:
    tf_backend_region: Optional[str]
    resource_group: Optional[str]
    subscription_id: Optional[str]
    tenant_id: Optional[str]
    tf_storage_account_name: Optional[str]
    application_id: Optional[str]


class ICloudConfig:
    cloud_provider: Optional[str]
    name: Optional[str]
    status: Optional[str]
    organization_uuid: Optional[str]
    custom_tags: Optional[dict]
    uuid: Optional[Union[str, UUID]]
    data: Optional[Union[IAwsProviderData, IAzureProviderData]]

    @abstractmethod
    def __call__(self, **data) -> ICloudConfig:
        raise NotImplementedError


class IAwsCloudConfig(ICloudConfig):
    data: IAwsProviderData


class IAzureCloudConfig(ICloudConfig):
    data: IAzureProviderData


class IGitRepoSource(ABC):
    type: str
    repo_url: str
    reference: Optional[str]
    username: str
    token: str


class IS3Source(ABC):
    type: str
    bucket_path: str
    bucket_region: str


class IWorkspaceSource(ABC):
    type: str
    path: str


class ITextSource(ABC):
    type: str


class IRetryStrategy(ABC):
    num_retries: int
    delay_between_retries: int
    retry_on_timeout: bool


class IJobConfig(ABC):
    type: Optional[str]
    source: Optional[Union[IGitRepoSource, IWorkspaceSource, IS3Source, ITextSource]]
    exec_file: Optional[str]
    exec_text: Optional[str]
    sql_query_parameters: Optional[dict]
    args: Optional[Union[dict, str]]
    retry_strategy: Optional[IRetryStrategy]
    timeout: Optional[int]
    env_vars: Optional[dict]
    catalog: Optional[str]


class IJobRun(ABC):
    def dict(self):
        super().dict()

    def __call__(self, **kwargs) -> "IJobRun":
        raise NotImplementedError

    uuid: Optional[str]
    name: Optional[str]
    type: Optional[str]
    submitted_at: Optional[datetime]
    finished_at: Optional[datetime]
    last_health_check: Optional[datetime]
    last_known_activity: Optional[datetime]
    status: Optional[str]
    reason: Optional[str]
    num_retries_used: Optional[int]
    tags: Optional[List]
    cluster_id: Optional[str]
    retry_strategy: Optional[IRetryStrategy]
    cluster: Optional[ICluster]
    cluster_config: Optional[ICluster]
    config: Optional[Union[dict, IJobConfig]]
    job_template_id: Optional[str]
    submitter: Optional[str]
    stats: Optional[dict]

    @abstractmethod
    def wait_for_status(self, statuses, timeout, tick) -> "IJobRun":
        raise NotImplementedError

    @abstractmethod
    def _save(self) -> IJobRun:
        raise NotImplementedError

    @property
    def id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _load(self) -> IJobRun:
        raise NotImplementedError

    @abstractmethod
    def cancel(self) -> IJobRun:
        raise NotImplementedError

    @abstractmethod
    def get_logs_urls(self) -> IJobRunLogsResponse:
        raise NotImplementedError

    @abstractmethod
    def get_stdout(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_stderr(self) -> str:
        raise NotImplementedError


class IJobTemplate(ABC):
    uuid: Optional[str]
    name: Optional[str]
    job_runs: List[IJobRun]
    description: Optional[str]
    created_by: Optional[str]
    config: Optional[IJobConfig]
    cluster_config: Optional[ICluster]

    @property
    def id(self):
        raise NotImplementedError

    def dict(self):
        return super().dict()

    @abstractmethod
    def __call__(self, **data) -> IJobTemplate:
        raise NotImplementedError

    @abstractmethod
    def run(
        self,
        name: str = None,
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
    ) -> IJobRun:
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError


class IInstanceRoleList(IBaseList):
    @abstractmethod
    def __call__(self, **data) -> "IInstanceRoleList":
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError


class IClusterList(IBaseList):
    @abstractmethod
    def __call__(self, **data) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def delete(self, wait=False) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def resume(self, wait=False) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def stop(self, wait=False) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def start(self, wait=False) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def pause(self, wait=False) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def refresh(self) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def wait_for_status(self, statuses, timeout, tick) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def run_job(
        self,
        template_id: str = None,
        code_type: str = None,
        source: Union[
            dict, IS3Source, IGitRepoSource, IWorkspaceSource, ITextSource
        ] = None,
        exec_file: str = None,
        args: Union[dict, str] = None,
        env_vars: dict = None,
        timeout: int = None,
        num_retries: int = None,
        delay_between_retries: int = None,
        retry_on_timeout: bool = None,
        name: str = None,
        catalog: str = None,
    ) -> IJobRunList:
        raise NotImplementedError

    @abstractmethod
    def run_sql_query(
        self,
        template_id: str = None,
        catalog: str = None,
        sql_query: str = None,
        name: str = None,
        args: dict = None,
        timeout: int = None,
        num_retries: int = None,
        delay_between_retries: int = None,
        retry_on_timeout: bool = None,
    ) -> IJobRunList:
        raise NotImplementedError

    @abstractmethod
    def cancel_jobs(self) -> IClusterList:
        raise NotImplementedError


class IJobTemplateFilter(ABC):
    ids: Optional[List[str]]
    names: Optional[List[str]]
    tags: Optional[Dict]


class IJobTemplateList(IBaseList):
    @abstractmethod
    def __call__(self, **data) -> "IJobTemplateList":
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def run(self, cluster: Union[dict, ICluster] = None) -> IJobRunList:
        raise NotImplementedError


class IJobRunList(IBaseList):
    page: Optional[int]
    page_size: Optional[int]
    total: Optional[int]
    order: Optional[Dict]
    filters: Optional[IJobFilter]
    _elements: List[IJobRun]

    @abstractmethod
    def __call__(self, **data) -> IJobRunList:
        raise NotImplementedError

    @abstractmethod
    def cancel(self) -> IJobRunList:
        raise NotImplementedError

    @abstractmethod
    def _load_next_page(self) -> IJobRunList:
        raise NotImplementedError

    @abstractmethod
    def wait_for_status(self, statuses, timeout, tick) -> IJobRunList:
        raise NotImplementedError

    @property
    def clusters(self) -> IClusterList:
        raise NotImplementedError


class IInstanceRole(ABC):
    uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    role_arn: Optional[str]
    status: Optional[str]

    @property
    def id(self):
        return self.uuid

    @abstractmethod
    def __call__(self, **data) -> IInstanceRole:
        raise NotImplementedError

    @abstractmethod
    def _save(self) -> IInstanceRole:
        raise NotImplementedError

    @abstractmethod
    def _load(self) -> IInstanceRole:
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError


class INodeMetadata(ABC):
    private_ip: Optional[str]
    instance_id: Optional[str]


class IClusterFilter(ABC):
    ids: Optional[List[str]]
    cluster_names: Optional[List[str]]
    statuses: Optional[List[str]]
    tags: Optional[List[str]]


class ICluster(ABC):
    name: Optional[str]
    id: Optional[str]
    status: Optional[str]
    description: Optional[str]
    instance_type: Optional[str]
    workers_quantity: Optional[int]
    auto_stop: Optional[int]
    auto_pause: Optional[int]
    bodo_version: Optional[str]
    image_id: Optional[str]
    cores_per_worker: Optional[int]
    accelerated_networking: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]
    is_job_dedicated: Optional[bool]
    auto_az: Optional[bool]
    use_spot_instance: Optional[bool]
    last_known_activity: Optional[str]
    in_state_since: Optional[str]
    cluster_agent_version: Optional[str]
    cluster_init_status: Optional[str]
    cluster_health_status: Optional[str]
    primary_agent_ip: Optional[str]
    aws_deployment_subnet_id: Optional[str]
    node_metadata: Optional[List[INodeMetadata]]
    availability_zone: Optional[str]
    instance_role: Optional[IInstanceRole]
    workspace: Optional[dict]
    autoscaling_identifier: Optional[str]
    last_asg_activity_id: Optional[str]
    nodes_ip: Optional[List[str]]

    def __call__(self, **kwargs) -> "ICluster":
        raise NotImplementedError

    def dict(self):
        return super().dict()

    @abstractmethod
    def run_job(
        self,
        template_id: str = None,
        code_type: str = None,
        source: Union[
            dict, IS3Source, IGitRepoSource, IWorkspaceSource, ITextSource
        ] = None,
        exec_file: str = None,
        args: Union[dict, str] = None,
        env_vars: dict = None,
        timeout: int = None,
        num_retries: int = None,
        delay_between_retries: int = None,
        retry_on_timeout: bool = None,
        name: str = None,
        catalog: str = None,
    ) -> IJobRun:  # TODO: add other fields and attribute typing
        raise NotImplementedError

    @abstractmethod
    def run_sql_query(
        self,
        template_id: str = None,
        catalog: str = None,
        sql_query: str = None,
        name: str = None,
        args: dict = None,
        timeout: int = None,
        num_retries: int = None,
        delay_between_retries: int = None,
        retry_on_timeout: bool = None,
    ) -> IJobRun:  # TODO: add other fields and attribute typing
        raise NotImplementedError

    @abstractmethod
    def cancel_jobs(self) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def _save(self) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def _load(self) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def stop(self, wait=False) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def start(self, wait=False) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def pause(self, wait=False) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def resume(self, wait=False) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def delete(self, force=False, mark_as_terminated=False, wait=False):
        raise NotImplementedError

    @abstractmethod
    def wait_for_status(self, statuses, timeout=600, tick=30) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        auto_stop: Optional[int] = None,
        auto_pause: Optional[int] = None,
        description: Optional[str] = None,
        name: Optional[str] = None,
        workers_quantity: Optional[int] = None,
        instance_role: Optional[IInstanceRole] = None,
        instance_type: Optional[str] = None,
        bodo_version: Optional[str] = None,
        auto_az: Optional[bool] = None,
        availability_zone: Optional[str] = None,
        custom_tags: Optional[Dict] = None,
    ) -> "ICluster":
        raise NotImplementedError

    @abstractmethod
    def connect(self, catalog: str) -> IConnection:
        raise NotImplementedError


class ICursor:
    @abstractmethod
    def execute(self, query: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def execute_async(self, query: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def fetchone(self):
        raise NotImplementedError

    @abstractmethod
    def fetchmany(self, size):
        raise NotImplementedError

    @abstractmethod
    def fetchall(self):
        raise NotImplementedError


class IConnection:
    @abstractmethod
    def cursor(self) -> ICursor:
        raise NotImplementedError


class IInstanceType:
    name: str
    vcpus: int
    cores: int
    memory: int
    efa: Optional[bool]
    accelerated_networking: Optional[bool]


class IClusterClient(ABC):
    _workspace_client: IBodoWorkspaceClient

    @property
    def Cluster(self) -> ICluster:
        raise NotImplementedError

    @property
    def ClusterList(self) -> "IClusterList":
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        name: str,
        instance_type: str = None,
        workers_quantity: int = None,
        description: Optional[str] = None,
        bodo_version: str = None,
        auto_stop: Optional[int] = None,
        auto_pause: Optional[int] = None,
        image_id: Optional[str] = None,
        accelerated_networking: Optional[bool] = None,
        auto_az: Optional[bool] = None,
        use_spot_instance: Optional[bool] = None,
        aws_deployment_subnet_id: Optional[str] = None,
        availability_zone: Optional[str] = None,
        instance_role: Optional[Union[IInstanceRole, Dict]] = None,
        custom_tags: Optional[Dict] = None,
    ) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        filters: Optional[Union[Dict, IClusterFilter]] = None,
        order: Optional[Dict] = None,
    ) -> IClusterList:
        raise NotImplementedError

    @abstractmethod
    def pause(self, id: str, wait=False) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def resume(self, id: str, wait=False) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def stop(self, id: str, wait=False) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def start(self, id: str, wait=False) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def remove(self, id: str, wait=False) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        auto_stop: Optional[int] = None,
        auto_pause: Optional[int] = None,
        workers_quantity: Optional[int] = None,
        instance_role: Optional[Union[IInstanceRole, Dict]] = None,
        instance_type: Optional[str] = None,
        bodo_version: Optional[str] = None,
        auto_az: Optional[bool] = None,
        availability_zone: Optional[str] = None,
        custom_tags: Optional[Dict] = None,
    ) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def scale(self, id: str, new_size: int) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def wait_for_status(
        self,
        id: str,
        statuses: List,
        timeout: Optional[int] = 300,
        tick: Optional[int] = 30,
    ) -> ICluster:
        raise NotImplementedError

    @abstractmethod
    def get_bodo_versions(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_images(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_instance_types(self) -> List[IInstanceType]:
        raise NotImplementedError

    @property
    def latest_bodo_version(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def connect(self, catalog: str, cluster_id: str) -> IConnection:
        raise NotImplementedError


class IJobFilter:
    ids: Optional[List[Union[str, UUID]]] = None
    template_ids: Optional[List[Union[str, UUID]]] = None
    cluster_ids: Optional[List[Union[str, UUID]]] = None
    types: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class IJobClient(ABC):
    _workspace_client: IBodoWorkspaceClient

    @property
    def JobRun(self) -> "IJobRun":
        raise NotImplementedError

    @property
    def JobRunList(self) -> "IJobRunList":
        raise NotImplementedError

    @abstractmethod
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
    ) -> "IJobRun":
        raise NotImplementedError

    @abstractmethod
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
    ) -> "IJobRun":
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str) -> "IJobRun":
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        filters: Optional[Union[Dict, IJobFilter]] = None,
        order: Optional[Dict] = None,
    ) -> "IJobRunList":
        raise NotImplementedError

    @abstractmethod
    def cancel_job(self, id: str) -> IJobRun:
        raise NotImplementedError

    @abstractmethod
    def cancel_jobs(self, filters: Optional[Union[Dict, IJobFilter]] = None) -> IJobRun:
        raise NotImplementedError

    @abstractmethod
    def wait_for_status(
        self, id: str, statuses: List, timeout: int = 3600, tick: int = 30
    ) -> abstractmethod:
        raise NotImplementedError


class IJobTemplateClient(ABC):
    _workspace_client: IBodoWorkspaceClient

    @property
    def JobTemplate(self) -> "IJobTemplate":
        raise NotImplementedError

    @property
    def JobTemplateList(self) -> "IJobTemplateList":
        raise NotImplementedError

    @abstractmethod
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
    ) -> IJobTemplate:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str) -> IJobTemplate:
        raise NotImplementedError

    @abstractmethod
    def remove(self, id: str) -> IJobTemplate:
        raise NotImplementedError

    @abstractmethod
    def list(self, filters: Dict) -> IJobTemplateList:
        raise NotImplementedError


class IWorkspace(ABC):
    @abstractmethod
    def delete(self, wait=False) -> IWorkspace:
        raise NotImplementedError

    @abstractmethod
    def update_infra(self) -> IWorkspace:
        raise NotImplementedError

    @abstractmethod
    def wait_for_status(self, statuses: List[str], timeout=600, tick=30) -> IWorkspace:
        raise NotImplementedError

    def __call__(self, **kwargs) -> "IWorkspace":
        raise NotImplementedError

    def dict(self):
        return super().dict()

    @abstractmethod
    def _load(self) -> IWorkspace:
        raise NotImplementedError

    @abstractmethod
    def _save(self) -> IWorkspace:
        raise NotImplementedError


class IJobRunLogsResponse(ABC):
    stderr_location_url: str
    stdout_location_url: str
    expiration_date: str


class ISnowflakeDetails(ABC):
    port: Optional[int]
    schema: Optional[str]
    database: Optional[str]
    user_role: Optional[str]
    username: Optional[str]
    warehouse: Optional[str]
    account_name: Optional[str]
    password: Optional[str]


class ICatalog(ABC):
    uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    catalog_type: Optional[str] = None
    details: Optional[Union[ISnowflakeDetails, dict]] = None

    @abstractmethod
    def __call__(self, **data) -> ICatalog:
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError


class ICatalogApi(ABC):
    def create(self, catalog: ICatalog) -> dict:
        raise NotImplementedError

    def get(self, uuid):
        raise NotImplementedError

    def get_by_name(self, name):
        raise NotImplementedError

    def get_all(
        self,
        page=None,
        page_size=None,
        names=None,
        uuids=None,
        order=None,
    ):
        raise NotImplementedError

    def update(self, catalog: ICatalog):
        raise NotImplementedError

    def delete(self, uuid):
        raise NotImplementedError

    def delete_all(self):
        raise NotImplementedError


class ICatalogClient(ABC):
    @property
    def Catalog(self) -> ICatalog:
        raise NotImplementedError

    @property
    def CatalogList(self) -> ICatalogList:
        raise NotImplementedError

    def list(self, filters: dict) -> ICatalogList:
        raise NotImplementedError

    def get(
        self,
        id: str,
    ) -> ICatalog:
        raise NotImplementedError

    def create(
        self,
        name: str,
        catalog_type: str,
        details: Union[ISnowflakeDetails, dict],
        description: Optional[str] = None,
    ) -> ICatalog:
        raise NotImplementedError

    def create_snowflake_catalog(
        self,
        name: str,
        details: Union[ISnowflakeDetails, dict],
        description: Optional[str] = None,
    ) -> ICatalog:
        raise NotImplementedError

    def delete(self, id: str):
        raise NotImplementedError


class ICatalogList(IBaseList):
    @abstractmethod
    def __call__(self, **data) -> ICatalogList:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError


class ICloudConfigList(IBaseList):
    @abstractmethod
    def __call__(self, **data) -> ICloudConfig:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError


class ICloudConfigApi(ABC):
    def create(self, cloud_config):
        raise NotImplementedError

    def update(self, cloud_config):
        raise NotImplementedError

    def list(self, page=None, page_size=None, order=None, provider=None, status=None):
        raise NotImplementedError

    def get(self, uuid):
        raise NotImplementedError

    def delete(self, uuid):
        raise NotImplementedError


class ISecretGroup:
    uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __call__(self, **data) -> ISecretGroup:
        raise NotImplementedError

    def _save(self) -> ISecretGroup:
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class ISecretGroupFilter:
    names: Optional[List[str]] = None


class ISecretGroupList(IBaseList):
    page: Optional[int]
    page_size: Optional[int]
    total: Optional[int]
    order: Optional[dict]
    filters: Optional[Union[ISecretGroupFilter, dict]]

    def __call__(self, **data) -> ISecretGroupList:
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class ISecret(ABC):
    uuid: Optional[str] = None
    name: Optional[str] = None
    secret_type: Optional[str] = None
    data: Optional[dict] = None
    secret_group: Optional[ISecretGroup] = None

    def __call__(self, **data) -> ISecret:
        raise NotImplementedError

    def _save(self) -> ISecret:
        raise NotImplementedError

    def _load(self) -> ISecret:
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class ISecretFilter(ABC):
    names: Optional[List[str]] = None
    secret_groups: Optional[List[str]] = None


class ISecretList(IBaseList):
    page: Optional[int]
    page_size: Optional[int]
    total: Optional[int]
    order: Optional[dict]
    filters: Optional[ISecretFilter]

    def __call__(self, **data) -> ISecretList:
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class ICatalogFilter:
    names: Optional[List[str]]
    ids: Optional[List[str]]


class ISecretsApi:
    def create_secret(self, secret: ISecret) -> dict:
        raise NotImplementedError

    def get_secret(self, uuid) -> dict:
        raise NotImplementedError

    def get_all_secrets(
        self, page=None, page_size=None, names=None, secret_groups=None, order=None
    ):
        raise NotImplementedError

    def get_all_secrets_by_group(self, secret_group: str):
        raise NotImplementedError

    def update_secret(self, secret: ISecret) -> dict:
        raise NotImplementedError

    def delete_secret(self, uuid):
        raise NotImplementedError


class ISecretGroupApi:
    def create_secret_group(self, secret_group: ISecretGroup) -> dict:
        raise NotImplementedError

    def get_secret_groups(
        self, page=None, page_size=None, names=None, order=None
    ) -> List[dict]:
        raise NotImplementedError

    def update_secret_group(self, secret_group: ISecretGroup) -> dict:
        raise NotImplementedError

    def delete_secret_group(self, name: str):
        raise NotImplementedError


class ISecretClient:
    @property
    def SecretGroup(self) -> ISecretGroup:
        raise NotImplementedError

    @property
    def SecretGroupList(self) -> ISecretGroup:
        raise NotImplementedError

    @property
    def Secret(self) -> ISecretGroup:
        raise NotImplementedError

    @property
    def SecretList(self) -> ISecretGroup:
        raise NotImplementedError

    def list_secret_groups(
        self, filters: Union[dict, ISecretGroupFilter] = None
    ) -> ISecretGroupList:
        raise NotImplementedError

    def list_secrets(self, filters: Union[dict, ISecretFilter] = None) -> ISecretList:
        raise NotImplementedError

    def get_secret(
        self,
        id: str,
    ) -> ISecret:
        raise NotImplementedError

    def create_secret(
        self,
        name: str,
        secret_type: str,
        data: dict,
        secret_group: ISecretGroup,
    ) -> ISecret:
        raise NotImplementedError

    def delete_secret(self, id: str):
        raise NotImplementedError

    def create_secret_group(
        self,
        name: str,
        description: str,
    ) -> ISecretGroup:
        raise NotImplementedError

    def delete_secret_group(self, name: str):
        raise NotImplementedError
