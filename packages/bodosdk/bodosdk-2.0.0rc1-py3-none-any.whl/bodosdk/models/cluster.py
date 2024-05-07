from __future__ import annotations
import time
from datetime import datetime
from typing import Optional, List, Union, Dict, Any

from pydantic import Field, ValidationError

from bodosdk.api.models.cluster import (
    ClusterDefinition,
    ModifyCluster,
)
from bodosdk.base import SDKBaseModel
from bodosdk.db.connection import Connection
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import ConflictException, TimeoutException, ResourceNotFound
from bodosdk.interfaces import (
    ICluster,
    IJobRun,
    IClusterList,
    IBodoWorkspaceClient,
    IClusterFilter,
    IJobRunList,
    IS3Source,
    IGitRepoSource,
    IWorkspaceSource,
    ITextSource,
    IInstanceType,
)
from bodosdk.models.instance_role import InstanceRole


class NodeMetadata(SDKBaseModel):
    private_ip: Optional[str] = Field(None, alias="privateIP")
    instance_id: Optional[str] = Field(None, alias="instanceId")


class Cluster(SDKBaseModel, ICluster):
    """
    Represents a cluster in the SDK model, encapsulating various properties and operations
    related to a compute cluster.

    Attributes:
        name (Optional[str]): The name of the cluster.
        uuid (Optional[str]): The unique identifier of the cluster.
        status (Optional[str]): The current status of the cluster (e.g., 'RUNNING', 'STOPPED').
        description (Optional[str]): A description of the cluster.
        instance_type (Optional[str]): The type of instances used in the cluster (e.g., 'c5.large').
        workers_quantity (Optional[int]): The number of worker nodes in the cluster.
        auto_stop (Optional[int]): The auto-stop configuration in minutes.
            The cluster automatically stops when idle for this duration.
        auto_pause (Optional[int]): The auto-pause configuration in minutes.
            The cluster automatically pauses when idle for this duration.
        bodo_version (Optional[str]): The version of Bodo being used in the cluster.
        image_id (Optional[str]): The ID of the image used for the cluster's instances.
        cores_per_worker (Optional[int]): The number of CPU cores per worker node.
        accelerated_networking (Optional[bool]): Whether accelerated networking is enabled.
        created_at (Optional[str]): The creation timestamp of the cluster.
        updated_at (Optional[str]): The last update timestamp of the cluster.
        is_job_dedicated (Optional[bool]): Whether the cluster is dedicated to a specific job.
        auto_az (Optional[bool]): Whether automatic availability zone selection is enabled.
        use_spot_instance (Optional[bool]): Whether spot instances are used for the cluster.
        last_known_activity (Optional[str]): The last known activity timestamp of the cluster.
        in_state_since (Optional[str]): The timestamp since the cluster has been in its current state.
        cluster_agent_version (Optional[str]): The version of the cluster agent.
        cluster_init_status (Optional[str]): The initialization status of the cluster.
        cluster_health_status (Optional[str]): The health status of the cluster.
        primary_agent_ip (Optional[str]): The IP address of the primary agent in the cluster.
        aws_deployment_subnet_id (Optional[str]): The subnet ID used for deploying AWS resources.
        node_metadata (Optional[List[NodeMetadata]]): Metadata information for each node in the cluster.
        availability_zone (Optional[str]): The AWS availability zone in which the cluster is located.
        instance_role (Optional[InstanceRole]): The IAM role used by instances in the cluster.
        workspace (Optional[dict]): A dictionary containing workspace-related information for the cluster.
        autoscaling_identifier (Optional[str]): The identifier for autoscaling configuration.
        last_asg_activity_id (Optional[str]): The identifier of the last activity in the autoscaling group.
        nodes_ip (Optional[List[str]]): A list of IP addresses for the nodes in the cluster.
    """

    name: Optional[str] = Field(None, alias="name")
    uuid: Optional[str] = Field(None, alias="uuid")
    status: Optional[str] = Field(None, alias="status")
    description: Optional[str] = Field(None, alias="description")
    instance_type: Optional[str] = Field(None, alias="instanceType")
    workers_quantity: Optional[int] = Field(None, alias="workersQuantity")
    auto_stop: Optional[int] = Field(None, alias="autoStop")
    auto_pause: Optional[int] = Field(None, alias="autoPause")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    image_id: Optional[str] = Field(None, alias="imageId")
    cores_per_worker: Optional[int] = Field(None, alias="coresPerWorker")
    accelerated_networking: Optional[bool] = Field(None, alias="acceleratedNetworking")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    is_job_dedicated: Optional[bool] = Field(None, alias="isJobDedicated")
    auto_az: Optional[bool] = Field(None, alias="autoAZ")
    use_spot_instance: Optional[bool] = Field(None, alias="useSpotInstance")
    last_known_activity: Optional[datetime] = Field(None, alias="lastKnownActivity")
    in_state_since: Optional[datetime] = Field(None, alias="inStateSince")
    cluster_agent_version: Optional[str] = Field(None, alias="clusterAgentVersion")
    cluster_init_status: Optional[str] = Field(None, alias="clusterInitStatus")
    cluster_health_status: Optional[str] = Field(None, alias="clusterHealthStatus")
    primary_agent_ip: Optional[str] = Field(None, alias="primaryAgentIP")
    aws_deployment_subnet_id: Optional[str] = Field(None, alias="awsDeploymentSubnetId")
    node_metadata: Optional[List[NodeMetadata]] = Field(None, alias="nodeMetadata")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    instance_role: Optional[InstanceRole] = Field(None, alias="instanceRole")
    workspace: Optional[dict] = Field(None, alias="workspace")
    autoscaling_identifier: Optional[str] = Field(None, alias="autoscalingIdentifier")
    last_asg_activity_id: Optional[str] = Field(None, alias="lastAsgActivityId")
    nodes_ip: Optional[List[str]] = Field(None, alias="nodesIp")
    custom_tags: Optional[Dict] = Field(default_factory=dict, alias="customTags")

    def __setattr__(self, key: str, value: Any):
        """
        Sets the value of an attribute using custom logic for 'node_metadata' and 'instance_role',
        ensuring they are correctly instantiated.

        Args:
            key: The name of the attribute to set.
            value: The value to assign to the attribute.

        Raises:
            ValueError: If provided data for 'instance_role' is invalid.
            TypeError: If 'node_metadata' is not a list of NodeMetadata instances or dictionaries.
        """
        if key == "node_metadata" and isinstance(value, list):
            processed_value = self._process_node_metadata(value)
            super().__setattr__(key, processed_value)
        elif key == "instance_role" and isinstance(value, dict):
            try:
                instance_role_value = (
                    self._workspace_client.InstanceRoleClient.InstanceRole(**value)
                )
                super().__setattr__(key, instance_role_value)
            except ValidationError as e:
                raise ValueError(f"Invalid data for InstanceRole: {e}")
        else:
            super().__setattr__(key, value)

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new Cluster instance.

        Args:
            workspace_client: An optional client for interacting with the workspace API.
            **data: Arbitrary keyword arguments representing cluster properties.
        """
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> Cluster:
        """
        Creates a new instance of the Cluster with the same workspace client and provided data.

        Args:
            **data: Arbitrary keyword arguments representing cluster properties.

        Returns:
            A new instance of Cluster.
        """
        c = Cluster(self._workspace_client, **data)
        if not c.bodo_version and not c.image_id:
            c._update(
                {
                    "bodo_version": self._workspace_client.ClusterClient.latest_bodo_version
                }
            )
        if c.instance_role:
            c.instance_role._workspace_client = self._workspace_client
        return c

    @property
    def id(self) -> str:
        """
        The UUID of the cluster.

        Returns:
            The UUID string of the cluster.
        """
        return self.uuid

    @id.setter
    def _(self, value):
        self.uuid = value

    def _process_node_metadata(self, value: List[Union[NodeMetadata, Dict]]):
        """
        Processes a list of node metadata, ensuring each item is a properly instantiated NodeMetadata object.

        Args:
            value: A list of dictionaries or NodeMetadata instances.

        Returns:
            A list of NodeMetadata instances.

        Raises:
            ValueError: If an item in the list cannot be converted to NodeMetadata.
            TypeError: If the input is not a list of NodeMetadata instances or dictionaries.
        """
        processed_value = []
        for item in value:
            if isinstance(item, dict):
                try:
                    node_metadata_item = NodeMetadata(**item)
                    processed_value.append(node_metadata_item)
                except ValidationError as e:
                    raise ValueError(f"Invalid data for NodeMetadata: {e}")
            elif isinstance(item, NodeMetadata):
                processed_value.append(item)
            else:
                raise TypeError(
                    "node_metadata must be a list of NodeMetadata instances or dictionaries"
                )
        return processed_value

    @check_deprecation
    def _save(self) -> Cluster:
        """
        Saves changes made to the cluster's configuration to the workspace, updating or creating
        the cluster as necessary.

        Returns:
            The updated Cluster instance.
        """
        if self._modified:
            if self.instance_role:
                if isinstance(self.instance_role, dict):
                    self._update(
                        {
                            "instance_role": self._workspace_client.InstanceRoleClient.InstanceRole(
                                **self.instance_role
                            )
                        }
                    )
                self.instance_role._save()
            if self.uuid:
                if self._modified_fields == {"workers_quantity"}:
                    resp = self._workspace_client._cluster_api.modify_cluster(
                        ModifyCluster(
                            uuid=self.uuid, workers_quantity=self.workers_quantity
                        )
                    )
                else:
                    resp = self._workspace_client._cluster_api.modify_cluster(
                        ModifyCluster(**self.dict())
                    )
            else:
                resp = self._workspace_client._cluster_api.create_cluster(
                    ClusterDefinition(**self.dict())
                )
            self._update(resp.dict())
            self._modified = False
        return self

    @check_deprecation
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
    ) -> IJobRun:
        """
        Submits a batch job for execution using specified configurations and resources.

        This method creates and dispatches a job within a computing cluster, allowing for extensive customization of
        execution parameters including source data, runtime environment, and failure handling strategies.

        Parameters:
            template_id (str, optional): Identifier for the job template to use.
            code_type (str, optional): Type of code to execute (e.g., Python, Java).
            source (Union[dict, IS3Source, IGitRepoSource, IWorkspaceSource, ITextSource], optional):
                Source of the code to be executed. Can be specified as a dictionary
                or an instance of one of the predefined source interfaces.
            exec_file (str, optional): Path to the executable file within the source.
            args (Union[dict, str], optional): Arguments to pass to the executable.
            Can be a string or a dictionary of parameters.
            env_vars (dict, optional): Environment variables to set for the job.
            timeout (int, optional): Maximum runtime (in seconds) before the job is terminated.
            num_retries (int, optional): Number of times to retry the job on failure.
            delay_between_retries (int, optional): Time to wait between retries.
            retry_on_timeout (bool, optional): Whether to retry the job if it times out.
            name (str, optional): Name of the job.
            catalog (str, optional): Catalog to log the job under.

        Returns:
            IJobRun: An object representing the submitted job, capable of providing status and results.

        """
        return self._workspace_client.JobClient.run(
            cluster=self,
            template_id=template_id,
            code_type=code_type,
            source=source,
            exec_file=exec_file,
            args=args,
            env_vars=env_vars,
            timeout=timeout,
            num_retries=num_retries,
            delay_between_retries=delay_between_retries,
            retry_on_timeout=retry_on_timeout,
            name=name,
            catalog=catalog,
        )

    @check_deprecation
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
    ) -> IJobRun:
        """
                Submits an SQL query for execution on the cluster, returning a job run object.

                This method handles the execution of an SQL query within a defined cluster environment.
                It supports customization of execution parameters such as query arguments,
                job name, execution timeouts, and retry strategies.

                Parameters:
                    template_id (str, optional): Identifier for the job template to use.
                    catalog (str, optional): Catalog under which to log the SQL job.
                    sql_query (str, optional): The SQL query string to be executed.
                    name (str, optional): Descriptive name for the SQL job.
                    args (dict, optional): Dictionary of arguments that are passed to the SQL query.
                    timeout (int, optional): Maximum allowable runtime in seconds before the job is terminated.
                    num_retries (int, optional): Number of times the job will be retried on failure.
                    delay_between_retries (int, optional): Interval in seconds between job retries.
                    retry_on_timeout (bool, optional): Whether to retry the job if it times out.

                Returns:
                    IJobRun: An object representing the status and result of the executed SQL job.
        `
        """
        return self._workspace_client.JobClient.run_sql_query(
            cluster=self,
            template_id=template_id,
            catalog=catalog,
            sql_query=sql_query,
            name=name,
            args=args,
            timeout=timeout,
            num_retries=num_retries,
            delay_between_retries=delay_between_retries,
            retry_on_timeout=retry_on_timeout,
        )

    @check_deprecation
    def cancel_jobs(self) -> Cluster:
        """
        Cancels all jobs associated with the cluster.

        Returns:
            The Cluster instance.
        """
        self._workspace_client.JobClient.cancel_jobs(
            filters={"cluster_ids": [self.uud]}
        )
        return self

    @check_deprecation
    def _load(self) -> Cluster:
        """
        Loads the current state of the cluster from the workspace.

        Returns:
            The updated Cluster instance.
        """
        resp = self._workspace_client._cluster_api.get_cluster(self.uuid)
        self._update(resp.dict())
        self._modified = False
        return self

    @check_deprecation
    def stop(self, wait: bool = False) -> Cluster:
        """
        Stops the cluster.

        Args:
            wait: If True, waits till cluster will be STOPPED.

        Returns:
            The Cluster instance with updated status.
        """
        resp = self._workspace_client._cluster_api.stop(self.uuid)
        self._update(resp.dict())
        if wait:
            self.wait_for_status(["STOPPED", "FAILED"])
        return self

    @check_deprecation
    def start(self, wait: bool = False) -> Cluster:
        """
        Starts the cluster.

        Args:
            wait: If True, waits till cluster will be RUNNING.

        Returns:
            The Cluster instance with updated status.
        """
        resp = self._workspace_client._cluster_api.restart(self.uuid)
        self._update(resp.dict())
        if wait:
            return self.wait_for_status(["RUNNING", "FAILED"])
        return self

    @check_deprecation
    def pause(self, wait: bool = False) -> Cluster:
        """
        Pauses the cluster if it is running.

        Args:
            wait: If True, waits till cluster will be PAUSED.

        Returns:
            The Cluster instance with updated status.

        Raises:
            ConflictException: If the cluster cannot be paused due to its current status.
        """
        if self.status in ["PAUSED", "PAUSING"]:
            if wait:
                return self.wait_for_status(["PAUSED", "FAILED"])
            return self
        if self.status in ["INITIALIZING", "RUNNING"] or not self.status:
            resp = self._workspace_client._cluster_api.pause(self.uuid)
            self._update(resp.dict())
            if wait:
                return self.wait_for_status(["PAUSED", "FAILED"])
            return self
        raise ConflictException("Cannot pause not RUNNING cluster")

    @check_deprecation
    def resume(self, wait: bool = False) -> Cluster:
        """
        Resumes the cluster if it was paused or stopped.

        Args:
            wait: If True, waits till cluster will be RUNNING.
        Returns:
            The Cluster instance with updated status.

        Raises:
            ConflictException: If the cluster cannot be resumed due to its current status.
        """
        if self.status == "PAUSED" or not self.status:
            resp = self._workspace_client._cluster_api.resume(self.uuid)
            self._update(resp.dict())
        elif self.status == "STOPPED" or not self.status:
            resp = self._workspace_client._cluster_api.restart(self.uuid)
            self._update(resp.dict())
        elif self.status not in ["RUNNING", "INITIALIZING"]:
            raise ConflictException(
                f"Cannot resume cluster {self.uuid} which is not PAUSED, current status: {self.status}"
            )
        if wait:
            return self.wait_for_status(["RUNNING", "FAILED"])
        return self

    @check_deprecation
    def delete(
        self, force: bool = False, mark_as_terminated: bool = False, wait: bool = False
    ) -> Cluster:
        """
        Deletes the cluster, optionally forcing removal or marking as terminated.

        Args:
            force: If True, forces the deletion of the cluster.
            mark_as_terminated: If True, marks the cluster as terminated instead of deleting.
            wait: If True, waits till cluster will be TERMINATED.
        Returns:
            The Cluster instance, potentially updated to reflect its new state.

        Handles:
            ResourceNotFound: Silently if the cluster is already deleted or not found.
        """
        try:
            resp = self._workspace_client._cluster_api.remove_cluster(
                self.uuid, force_remove=force, mark_as_terminated=mark_as_terminated
            )
            self._update(resp.dict())
            if wait:
                return self.wait_for_status(["TERMINATED", "FAILED"])
            return self
        except ResourceNotFound:
            self._mutable = True
            self.status = "TERMINATED"
            self._mutable = False
            return self

    @check_deprecation
    def wait_for_status(
        self, statuses: List[str], timeout: int = 600, tick: int = 30
    ) -> Cluster:
        """
        Waits for the cluster to reach one of the specified states within a given timeout.

        Args:
            statuses: A list of states to wait for.
            timeout: The maximum time to wait before raising a TimeoutException.
            tick: The interval between checks.

        Returns:
            The Cluster instance, once it has reached one of the desired states.

        Raises:
            TimeoutException: If the cluster does not reach a desired state within the timeout.
        """
        if "FAILED" not in statuses:
            statuses.append("FAILED")
        try:
            self._load()
        except ResourceNotFound:  # If resource not found then cluster is TERMINATED
            if "TERMINATED" in statuses:
                self._mutable = True
                self.status = "TERMINATED"
                self._mutable = False
                return self
            raise
        start_time = time.time()  # Record the start time
        while self.status not in statuses:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self._load()

            # Check if timeout is reached
            if elapsed_time > timeout:
                raise TimeoutException(
                    f"Cluster {self.uuid} wait for states {statuses} timeout! Current state: {self.status}"
                )
            time.sleep(tick)
        return self

    @check_deprecation
    def update(
        self,
        auto_stop: Optional[int] = None,
        auto_pause: Optional[int] = None,
        description: Optional[str] = None,
        name: Optional[str] = None,
        workers_quantity: Optional[int] = None,
        instance_role: Optional[InstanceRole] = None,
        instance_type: Optional[str] = None,
        bodo_version: Optional[str] = None,
        auto_az: Optional[bool] = None,
        availability_zone: Optional[str] = None,
        custom_tags: Optional[Dict] = None,
    ) -> Cluster:
        """
        Updates the cluster's configuration with the provided values.

        Args:
            auto_stop: Optional; configures auto-stop feature.
            auto_pause: Optional; configures auto-pause feature.
            description: Optional; updates the cluster's description.
            name: Optional; updates the cluster's name.
            workers_quantity: Optional; updates the number of workers.
            instance_role: Optional; updates the instance role.
            instance_type: Optional; updates the instance type.
            bodo_version: Optional; updates the Bodo version.
            auto_az: Optional; enables/disables automatic availability zone selection.
            availability_zone: Optional; sets a specific availability zone.

        Returns:
            The updated Cluster instance.
        """
        local_vars = locals().copy()
        local_vars.pop("self", None)
        cleaned_dict = {k: v for k, v in local_vars.items() if v is not None}
        if isinstance(cleaned_dict.get("instance_role", None), dict):
            cleaned_dict[
                "instance_role"
            ] = self._workspace_client.InstanceRoleClient.InstanceRole(
                **cleaned_dict["instance_role"]
            )
        self._update(cleaned_dict)._save()
        return self

    @check_deprecation
    def connect(self, catalog: str) -> Connection:
        """
        Establishes a connection to the specified catalog from Cluster.

        This method is responsible for creating and returning a new `Connection` instance based on the provided catalog.

        Parameters:
        catalog (str): The name of the catalog to which the connection should be established.

        Returns:
        Connection: An instance of `Connection` initialized with the specified catalog and the current class instance.

        """
        return Connection(catalog, self)


class ClusterFilter(SDKBaseModel, IClusterFilter):
    """
    Represents a filter used to select clusters based on specific criteria.

    This class is used to construct filter criteria for querying clusters by their identifiers,
    names, statuses, or tags. It inherits from `SDKBaseModel` and implements the `IClusterFilter` interface.

    Attributes:
        ids (Optional[List[str]]): Optional list of cluster UUIDs. Default is an empty list.
        cluster_names (Optional[List[str]]): Optional list of cluster names to filter by. Default is an empty list.
        statuses (Optional[List[str]]): Optional list of cluster statuses to filter by. Default is an empty list.
        tags (Optional[Dict]): Optional dictionary of tags for more fine-grained filtering.
        Default is an empty dictionary.

    Each attribute supports being set via their field name or by the specified alias in the Field definition.

    """

    class Config:
        """
        Configuration for Pydantic models.
        https://docs.pydantic.dev/latest/api/config/
        """

        extra = "forbid"
        allow_population_by_field_name = True

    ids: Optional[List[str]] = Field(default_factory=list, alias="uuids")
    cluster_names: Optional[List[str]] = Field(
        default_factory=list, alias="clusterNames"
    )
    statuses: Optional[List[str]] = Field(default_factory=list, alias="statues")
    tags: Optional[Dict] = Field(default_factory=dict, alias="tags")


class ClusterList(IClusterList, SDKBaseModel):
    """
    A model representing a list of clusters, providing pagination, filtering, and
    operations on clusters such as start, stop, delete, resume, and pause.

    Attributes:
        page (Optional[int]): The current page number for pagination, starting from 0.
        page_size (Optional[int]): The number of items to be displayed per page.
        total (Optional[int]): The total number of items available across all pages.
        order (Optional[Dict]): Ordering information for listing clusters. Defaults to an empty dict.
        filters (Optional[ClusterFilter]): Filtering criteria to apply when fetching the cluster list.
        _clusters (List[ICluster]): Internal list of cluster objects.
        _index (int): Internal index to track the current position when iterating through clusters.

    """

    class Config:
        """
        Configuration for Pydantic models.
        https://docs.pydantic.dev/latest/api/config/
        """

        extra = "forbid"
        allow_population_by_field_name = True

    page: Optional[int] = Field(0, alias="page")
    page_size: Optional[int] = Field(10, alias="pageSize")
    total: Optional[int] = Field(None, alias="total")
    order: Optional[Dict] = Field(default_factory=dict, alias="order")
    filters: Optional[Union[ClusterFilter, dict]] = Field(None, alias="filters")
    _elements: List
    _index: int = 0

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new instance of ClusterList with optional parameters for
        configuration and a workspace client for API interactions.

        Args:
            workspace_client (IBodoWorkspaceClient, optional): The client used for workspace API calls.
                This client is responsible for fetching cluster data from the backend.
            **data: Arbitrary keyword arguments that can be used to set the values of the model fields
                upon initialization.
        """
        super().__init__(**data)
        self._elements = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> ClusterList:
        """
        Creates and returns a new instance of ClusterList, optionally populated with
        the given data. This method is typically used for re-initializing or refreshing
        the list with new parameters or criteria.

        Args:
            **data: Arbitrary keyword arguments for configuring the new ClusterList instance.

        Returns:
            ClusterList: A new instance of ClusterList with the given configuration.
        """
        if "filters" in data and isinstance(data["filters"], dict):
            data["filters"] = ClusterFilter(**data["filters"])
        clusters_list = ClusterList(self._workspace_client, **data)
        return clusters_list._load_next_page()

    def __iter__(self) -> Cluster:
        """
        Provides an iterator over the clusters in the list. It supports iteration
        through the clusters, automatically loading the next page of clusters when
        necessary.

        Returns:
            Iterator[ICluster]: An iterator over the cluster objects in the list.
        """
        yield from super().__iter__()

    def _load_next_page(self) -> ClusterList:
        """
        Loads the next page of clusters from the workspace API, updating the internal
        list of clusters and the total item count. This method modifies the instance
        in place and is usually called automatically during iteration or when accessing
        items beyond the current page.
        """
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._cluster_api.get_all_clusters(
            page=self.page,
            page_size=self.page_size,
            order="ASC",
            cluster_names=self.filters.cluster_names if self.filters else None,
            uuids=self.filters.ids if self.filters else None,
            statuses=self.filters.statuses if self.filters else None,
            ordering=self.order,
            tags=self.filters.tags if self.filters else None,
        )
        self._deprecated_fields.update(
            resp._deprecated_fields if isinstance(resp._deprecated_fields, dict) else {}
        )
        self._deprecated_methods.update(
            resp._deprecated_methods
            if isinstance(resp._deprecated_methods, dict)
            else {}
        )
        if self.filters:
            self.filters._deprecated_fields.update(
                self._deprecated_fields.get("filters", {}).get("_deprecated_fields", {})
            )
            self.filters._deprecated_methods.update(
                self._deprecated_methods.get("filters", {}).get(
                    "_deprecated_methods", {}
                )
            )
        self._elements.extend(
            [
                self._workspace_client.ClusterClient.Cluster(**c.dict())
                for c in resp.data
            ]
        )
        self.total = resp.metadata.total_items
        self._mutable = False
        return self

    def __len__(self) -> int:
        """
        Returns the total number of clusters available across all pages, according
        to the last known state from the workspace API.

        Returns:
            int: The total number of clusters available.
        """
        return super().__len__()

    def __getitem__(self, key) -> Union[Cluster, List[Cluster]]:
        """
        Supports accessing individual clusters or a slice of clusters from the list,
        handling pagination transparently. This method enables indexing and slicing
        operations.

        Args:
            key (int | slice): The index or slice indicating which clusters to access.

        Returns:
            Union[ICluster, List[ICluster]]: A single cluster or a list of clusters, depending
                on the type of key provided.

        Raises:
            IndexError: If the key is out of the bounds of the cluster list.
        """
        return super().__getitem__(key)

    def __contains__(self, obj) -> bool:
        """
        Checks if a specific cluster is present in the current list of clusters.

        Args:
            obj: The cluster object to check for presence in the list.

        Returns:
            bool: True if the cluster is present in the list; False otherwise.
        """
        return super().__contains__(obj)

    @check_deprecation
    def delete(self, wait=False) -> ClusterList:
        """
        Deletes each cluster in the list, updating the internal list with the result
        of each delete operation. This method effectively attempts to delete all clusters
        and returns the updated list.

        Returns:
            ClusterList: The current instance of ClusterList after attempting to delete
                all clusters.
        """
        fresh_clusters = [cluster.delete() for cluster in self]
        self._elements = fresh_clusters
        if wait:
            return self.wait_for_status(["TERMINATED", "FAILED"])
        return self

    @check_deprecation
    def resume(self, wait=False) -> ClusterList:
        """
        Attempts to resume each paused or stopped cluster in the list. It handles exceptions
        gracefully, ensuring the list is updated with the status of each cluster after
        the operation.

        Returns:
            ClusterList: The current instance of ClusterList after attempting to resume
                all clusters.
        """
        fresh_clusters = []
        for cluster in self:
            try:
                fresh_clusters.append(cluster.resume())
            except ConflictException:
                fresh_clusters.append(cluster)
        self._elements = fresh_clusters
        if wait:
            return self.wait_for_status(["RUNNING", "FAILED"])
        return self

    @check_deprecation
    def stop(self, wait=False) -> ClusterList:
        """
        Attempts to stop each running or starting cluster in the list. It handles exceptions
        gracefully, updating the list with the status of each cluster after the operation.

        Returns:
            ClusterList: The current instance of ClusterList after attempting to stop
                all clusters.
        """
        fresh_clusters = []
        for cluster in self:
            try:
                fresh_clusters.append(cluster.stop())
            except ConflictException:
                fresh_clusters.append(cluster)
        self._elements = fresh_clusters
        if wait:
            return self.wait_for_status(["STOPPED", "FAILED"])
        return self

    @check_deprecation
    def start(self, wait=False) -> ClusterList:
        """
        Attempts to start each stopped or paused cluster in the list. It handles exceptions
        gracefully, ensuring the list reflects the status of each cluster after the operation.

        Returns:
            ClusterList: The current instance of ClusterList after attempting to start
                all clusters.
        """
        fresh_clusters = []
        for cluster in self:
            try:
                fresh_clusters.append(cluster.start())
            except ConflictException:
                fresh_clusters.append(cluster)
        self._elements = fresh_clusters
        if wait:
            return self.wait_for_status(["RUNNING", "FAILED"])
        return self

    @check_deprecation
    def pause(self, wait=False) -> ClusterList:
        """
        Attempts to pause each running cluster in the list. It handles exceptions gracefully,
        updating the list with the status of each cluster following the operation.

        Returns:
            ClusterList: The current instance of ClusterList after attempting to pause
                all clusters.
        """
        fresh_clusters = []
        for cluster in self:
            try:
                fresh_clusters.append(cluster.pause())
            except ConflictException:
                fresh_clusters.append(cluster)
        self._elements = fresh_clusters
        if wait:
            return self.wait_for_status(["PAUSED", "FAILED"])
        return self

    @check_deprecation
    def refresh(self) -> ClusterList:
        """
        Refreshes the list of clusters by resetting the pagination and filter settings,
        then reloading the first page of clusters. This method effectively resets the
        ClusterList instance to its initial state, based on current filters and ordering.

        Returns:
            ClusterList: The current instance of ClusterList after reloading the first page
                of clusters.
        """
        self._mutable = True
        self._index = 0
        self.page = 0
        self._elements = []
        self._load_next_page()
        self._mutable = False
        return self

    @check_deprecation
    def wait_for_status(
        self, statuses: List[str] = None, timeout: int = 600, tick: int = 60
    ) -> ClusterList:
        """
        Waits for each cluster in the list to reach one of the specified statuses, updating
        the list with the results. This method polls each cluster's status until it matches
        one of the desired statuses or until the timeout is reached.

        Args:
            statuses (List[str], optional): A list of status strings to wait for.
            timeout (int, optional): The maximum time to wait for each cluster to reach the
                desired status, in seconds.
            tick (int, optional): The interval between status checks, in seconds.

        Returns:
            ClusterList: The current instance of ClusterList after waiting for all clusters
                to reach one of the specified statuses.
        """
        fresh_clusters = []
        for cluster in self:
            fresh_clusters.append(cluster.wait_for_status(statuses, timeout, tick))
        self._elements = fresh_clusters
        return self

    @check_deprecation
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
        """
        Executes a job across all clusters managed by the instance.

        This method supports multiple source types and configurations for executing jobs,
        including retries and custom environment variables.

        Parameters:
            template_id (str, optional): Identifier for the job template to be used.
            code_type (str, optional): The type of code to execute (e.g., Python, Java).
            source (Union[dict, IS3Source, IGitRepoSource, IWorkspaceSource, ITextSource], optional):
            The source from where the job's code will be retrieved.
            exec_file (str, optional): Path to the main executable file within the source.
            args (Union[dict, str], optional): Arguments to pass to the job. Can be a dictionary or a
            string formatted as required by the job.
            env_vars (dict, optional): Environment variables to set for the job execution.
            timeout (int, optional): Maximum time in seconds for the job to run before it is terminated.
            num_retries (int, optional): Number of times to retry the job on failure.
            delay_between_retries (int, optional): Time in seconds to wait between retries.
            retry_on_timeout (bool, optional): Whether to retry the job if it times out.
            name (str, optional): A name for the job run.
            catalog (str, optional): Catalog identifier to specify a data catalog for the job.

        Returns:
            IJobRunList: An object listing the UUIDs of jobs that were successfully initiated.

        Decorators:
            @check_deprecation: Checks if the method or its parameters are deprecated.

        """
        job_uuids = []
        for cluster in self:
            job = cluster.run_job(
                template_id=template_id,
                code_type=code_type,
                source=source,
                exec_file=exec_file,
                args=args,
                env_vars=env_vars,
                timeout=timeout,
                num_retries=num_retries,
                delay_between_retries=delay_between_retries,
                retry_on_timeout=retry_on_timeout,
                name=name,
                catalog=catalog,
            )
            job_uuids.append(job.uuid)
        return self._workspace_client.JobClient.JobRunList(filters={"ids": job_uuids})

    @check_deprecation
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
        """
        Executes an SQL job across all clusters managed by the instance.

        This method submits an SQL query for execution, allowing for additional configurations such as retries
        and setting execution timeouts.

        Parameters:
            template_id (str, optional): Identifier for the job template to be used.
            catalog (str, optional): Catalog identifier to specify a data catalog for the SQL job.
            sql_query (str, optional): The SQL query to execute.
            name (str, optional): A name for the job run.
            args (dict, optional): Additional arguments specific to the SQL job.
            timeout (int, optional): Maximum time in seconds for the job to run before it is terminated.
            num_retries (int, optional): Number of times to retry the job on failure.
            delay_between_retries (int, optional): Time in seconds to wait between retries.
            retry_on_timeout (bool, optional): Whether to retry the job if it times out.

        Returns:
            IJobRunList: An object listing the UUIDs of SQL jobs that were successfully initiated.

        Decorators:
            @check_deprecation: Checks if the method or its parameters are deprecated.

        """
        job_uuids = []
        for cluster in self:
            job = cluster.run_sql_query(
                template_id=template_id,
                catalog=catalog,
                sql_query=sql_query,
                name=name,
                args=args,
                timeout=timeout,
                num_retries=num_retries,
                delay_between_retries=delay_between_retries,
                retry_on_timeout=retry_on_timeout,
            )
            job_uuids.append(job.uuid)
        return self._workspace_client.JobClient.JobRunList(filters={"ids": job_uuids})

    @check_deprecation
    def cancel_jobs(self) -> ClusterList:
        """
        Cancels all jobs associated with the clusters.

        Returns:
            The ClusterList instance.
        """
        cluster_uuids = []
        for cluster in self:
            cluster_uuids.append(cluster.uuid)
        self._workspace_client.JobClient.cancel_jobs(
            filters={"cluster_ids": cluster_uuids}
        )
        return self


class BodoImage(SDKBaseModel):
    """
    Represents an image configuration for Bodo, encapsulating the image ID and the specific Bodo version.

    This class is a data model that holds information about a Bodo environment image.

    Attributes:
        image_id (str): The unique identifier for the Bodo image.
        bodo_version (str): The version of Bodo used in the image.
    """

    image_id: str
    bodo_version: str


class InstanceType(SDKBaseModel, IInstanceType):
    """
    Represents the specifications for a type of computing instance.

    This class defines a specific configuration of a computing instance,
    including its processing power and memory capabilities, as well as optional features related to networking.

    Attributes:
        name (str): The name or identifier of the instance type.
        vcpus (int): The number of virtual CPUs available in this instance type.
        cores (int): The number of physical cores available in this instance type.
        memory (int): The amount of RAM (in megabytes) available in this instance type.
        efa (Optional[bool]): Indicates whether Elastic Fabric Adapter (EFA) is supported. Defaults to None.
        accelerated_networking (Optional[bool]): Specifies if accelerated networking is enabled.
        This is mapped to the JSON key 'acceleratedNetworking'. Defaults to None.

    """

    name: str
    vcpus: int
    cores: int
    memory: int
    efa: Optional[bool] = None
    accelerated_networking: Optional[bool] = Field(None, alias="acceleratedNetworking")
