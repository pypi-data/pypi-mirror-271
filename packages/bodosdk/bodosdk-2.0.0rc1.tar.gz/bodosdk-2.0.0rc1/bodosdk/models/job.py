from __future__ import annotations

import time
from datetime import datetime

from typing import Optional, Union, List, Any, Dict
from uuid import UUID

import requests
from pydantic import Field

from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.exceptions import TimeoutException
from bodosdk.interfaces import (
    IJobConfig,
    IJobRun,
    IBodoWorkspaceClient,
    IJobRunList,
    IJobTemplateFilter,
    IJobTemplateList,
    IJobTemplate,
    ICluster,
    IS3Source,
    IGitRepoSource,
    IWorkspaceSource,
    ITextSource,
    IJobRunLogsResponse,
)


class RetryStrategy(SDKBaseModel):
    """
    A Pydantic model that defines the retry strategy for a job or a task. It specifies how many retries
    should be attempted,
    the delay between retries, and whether to retry on timeout.

    Attributes:
        num_retries (int): The number of times to retry the job after a failure. Defaults to 0, meaning no
        retries by default.
        delay_between_retries (int): The delay between consecutive retries, expressed in minutes. Defaults to 1 minute.
        retry_on_timeout (bool): A flag to determine if the job should be retried upon timing out. Defaults to False,
        indicating no retry on timeout.

    Each field is represented with a default value and an alias that matches the corresponding key in JSON or
    other serialized forms.
    """

    num_retries: int = Field(0, alias="numRetries")
    delay_between_retries: int = Field(1, alias="delayBetweenRetries")  # in minutes
    retry_on_timeout: bool = Field(False, alias="retryOnTimeout")


class GitRepoSource(SDKBaseModel):
    """
    Git repository source definition.

    ...

    Attributes
    ----------
    repo_url: str
        Git repository URL.

    reference: Optional[str]
        Git reference (branch, tag, commit hash). (Default: "")

    username: str
        Git username.

    token: str
        Git token.

    """

    type: str = Field("GIT", const=True)
    repo_url: str = Field(..., alias="repoUrl")
    reference: Optional[str] = ""
    username: str
    token: str


class S3Source(SDKBaseModel):
    """
    S3 source definition.

    ...

    Attributes
    ----------
    bucket_path: str
        S3 bucket path.

    bucket_region: str
        S3 bucket region.

    """

    type: str = Field("S3", const=True)
    bucket_path: str = Field(..., alias="bucketPath")
    bucket_region: str = Field(..., alias="bucketRegion")


class WorkspaceSource(SDKBaseModel):
    """
    Workspace source definition.

    ...

    Attributes
    ----------
    path: str
        Workspace path.
    """

    type: str = Field("WORKSPACE", const=True)
    path: str


class TextSource(SDKBaseModel):
    """
    Represents a specific type of source where the job configuration can originate from a text source.

    Attributes:
        type (str): Specifies the type of source
    """

    type: str = Field("SQL", const=True)


class JobConfig(SDKBaseModel, IJobConfig):
    """
    Configures details for executing a job, including the execution source, file location, and execution parameters.

    Attributes:
        type (Optional[str]): The type of job: PYTHON, SQL, IPYNB
        source (Optional[Union[GitRepoSource, WorkspaceSource, S3Source, TextSource]]):
        The source from which the job is configured or executed.
        exec_file (Optional[str]): The location of the file to execute.
        exec_text (Optional[str]): The text containing script/code/sql to execute, valid for TextSource
        sql_query_parameters (Optional[dict]): Parameters to substitute within an SQL query.
        args (Optional[Union[dict, str]]): Additional arguments required for job execution.
        Can be a dictionary or string.
        retry_strategy (Optional[RetryStrategy]):
        Configuration for the job retry strategy.
        timeout (Optional[int]): The maximum time (in seconds) allowed for the job to run before it times out.
        env_vars (Optional[dict]): Environment variables to be set for the job run.
        catalog (Optional[str]): The catalog associated with the job, if applicable.
    """

    type: Optional[str]
    source: Optional[Union[GitRepoSource, WorkspaceSource, S3Source, TextSource]]
    exec_file: Optional[str] = Field(None, alias="sourceLocation")
    exec_text: Optional[str] = Field(None, alias="sqlQueryText")
    sql_query_parameters: Optional[dict] = Field(None, alias="sqlQueryParameters")
    args: Optional[Union[dict, str]]
    retry_strategy: Optional[RetryStrategy] = Field(None, alias="retryStrategy")
    timeout: Optional[int]
    env_vars: Optional[dict] = Field(None, alias="envVars")
    catalog: Optional[str]


class JobRun(SDKBaseModel, IJobRun):
    """
    Details a specific instance of a job run, including status and configuration details.

    Attributes:
        uuid (Optional[str]): Unique identifier for the job run.
        name (Optional[str]): Name of the job run.
        type (Optional[str]): Type of job run, defaults to 'BATCH' if not specified.
        submitted_at (Optional[datetime]): Timestamp when the job was submitted.
        finished_at (Optional[datetime]): Timestamp when the job finished running.
        last_health_check (Optional[datetime]): Timestamp of the last health check performed.
        last_known_activity (Optional[datetime]): Timestamp of the last known activity of this job.
        status (Optional[str]): Current status of the job run.
        reason (Optional[str]): Reason for the job's current status, particularly if there's an error or failure.
        num_retries_used (Optional[int]): The number of retries that have been used for this job run. Defaults to 0.
        tags (Optional[List]): Tags associated with the job run. Default is an empty list.
        cluster_uuid (Optional[str]): UUID of the cluster on which the job is running.
        cluster (Optional[Cluster]): The cluster object associated with the job run.
        cluster_config (Optional[Cluster]): Configuration of the cluster used for this job run.
        config (Optional[JobConfig]): Job configuration details used for this run.
        job_template_id (Optional[str]): UUID of the template from which this job was created.
        submitter (Optional[str]): The identifier of the user who submitted the job.
        stats (Optional[dict]): Statistical data about the job run.
    """

    uuid: Optional[str]
    name: Optional[str]
    type: Optional[str] = "BATCH"
    submitted_at: Optional[datetime] = Field(None, alias="submittedAt")
    finished_at: Optional[datetime] = Field(None, alias="finishedAt")
    last_health_check: Optional[datetime] = Field(None, alias="lastHealthCheck")
    last_known_activity: Optional[datetime] = Field(None, alias="lastKnownActivity")
    status: Optional[str]
    reason: Optional[str]
    num_retries_used: Optional[int] = (Field(0, alias="numRetriesUsed"),)
    tags: Optional[List] = Field(default_factory=list, alias="tag")
    cluster_id: Optional[str] = Field(None, alias="clusterUUID")
    cluster: Optional["Cluster"]
    cluster_config: Optional["Cluster"] = Field(None, alias="clusterConfig")
    config: Optional[Union[JobConfig]]
    job_template_id: Optional[str] = Field(None, alias="jobTemplateUUID")
    submitter: Optional[str]
    stats: Optional[dict]

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new JobRun instance.

        Args:
            workspace_client: An optional client for interacting with the workspace API.
            **data: Arbitrary keyword arguments representing cluster properties.
        """
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> JobRun:
        if "config" in data and isinstance(data["config"], dict):
            data["config"] = JobConfig(**data["config"])
        if "num_retries_used" not in data or "numRetriesUsed" not in data:
            data["num_retries_used"] = 0
        if "cluster_config" in data and isinstance(data["cluster_config"], dict):
            data["cluster_config"] = self._workspace_client.ClusterClient.Cluster(
                **data["cluster_config"]
            )
        if "cluster" in data and isinstance(data["cluster"], dict):
            data["cluster"] = self._workspace_client.ClusterClient.Cluster(
                **data["cluster"]
            )
        if "job_template" in data and isinstance(data["job_template"], dict):
            data["job_template"] = self._workspace_client.JobTemplateClient.JobTemplate(
                **data["job_template"]
            )
        return JobRun(self._workspace_client, **data)

    def __setattr__(self, key: str, value: Any):
        if key == "retry_strategy" and isinstance(value, dict):
            processed_value = RetryStrategy(**value)
            super().__setattr__(key, processed_value)
        elif key == "config" and isinstance(value, dict):
            processed_value = JobConfig(**value)
            super().__setattr__(key, processed_value)
        elif key in ("cluster", "cluster_config") and isinstance(value, dict):
            processed_value = self._workspace_client.ClusterClient.Cluster(**value)
            super().__setattr__(key, processed_value)
        elif key == "job_template" and isinstance(value, dict):
            processed_value = self._workspace_client.JobTemplateClient.JobTemplate(
                **value
            )
            super().__setattr__(key, processed_value)
        else:
            super().__setattr__(key, value)

    @check_deprecation
    def _save(self) -> JobRun:
        if self._modified and not self.uuid:
            resp = self._workspace_client._job_api.create_job_run(self)
            resp["config"]["source"] = resp["config"]["source"]["sourceDef"]
            self._update(resp)
            self._modified = False
        return self

    @check_deprecation
    def wait_for_status(
        self, statuses: List[str], timeout: int = 3600, tick: int = 30
    ) -> JobRun:
        """
        Waits for the job to reach one of the specified statuses, polling at regular intervals.

        This method checks the current status of the job at regular intervals defined by the `tick` parameter.
        If the job reaches one of the specified statuses before the timeout, it returns the job instance.
        If the timeout is exceeded, it raises a `TimeoutException`.

        Parameters:
            statuses (list or tuple): A list or tuple of statuses that the job is expected to reach.
            timeout (int, optional): The maximum time in seconds to wait for the job to reach one of
            the specified statuses. Defaults to 600 seconds.
            tick (int, optional): The time interval in seconds between status checks. Defaults to 30 seconds.

        Returns:
            JobRun: The job instance if one of the specified statuses is reached within the timeout period.

        Raises:
            TimeoutException: If the job does not reach one of the specified statuses within
            the specified timeout period.

        Decorators:
            @check_deprecation: Checks if the method or its parameters are deprecated.

        """
        if "FAILED" not in statuses:
            statuses.append("FAILED")
        if "CANCELLED" not in statuses:
            statuses.append("CANCELLED")
        self._load()
        start_time = time.time()  # Record the start time
        while self.status not in statuses:
            current_time = time.time()
            elapsed_time = current_time - start_time
            self._load()
            # Check if timeout is reached
            if elapsed_time > timeout:
                raise TimeoutException(
                    f"Job {self.uuid} wait for states {statuses} timeout! Current state: {self.status}"
                )
            time.sleep(tick)
        return self

    @property
    def id(self) -> str:
        return self.uuid

    @check_deprecation
    def _load(self) -> JobRun:
        resp = self._workspace_client._job_api.get_job(self.uuid)
        self._update(resp)
        self._modified = False
        return self

    @check_deprecation
    def cancel(self) -> JobRun:
        """
        Cancels the job associated with this instance and updates its state based on the response from the job API.

        This method sends a cancellation request for the job identified by its UUID to the job API,
        handles the response to update the job's attributes, and resets its modified state.

        Returns:
            JobRun: The job instance, updated with the latest state after the cancellation attempt.

        Raises:
            APIException: If the cancellation request fails or returns an error response.

        Decorators:
            @check_deprecation: Checks if the method or its parameters are deprecated.

        """
        resp = self._workspace_client._job_api.cancel_job(self.uuid)
        self._update(resp)
        self._modified = False
        return self

    @check_deprecation
    def get_logs_urls(self) -> JobRunLogsResponse:
        if self.id and self.status in ("FAILED", "CANCELLED", "SUCCEEDED"):
            resp = self._workspace_client._job_api.get_job_log_links(self.id, True)
            if resp:
                return JobRunLogsResponse(**resp.dict())

    @check_deprecation
    def get_stdout(self) -> str:
        logs = self.get_logs_urls()
        if logs and logs.stdout_location_url:
            response = requests.get(logs.stdout_location_url)
            if response.status_code == 200:
                return response.text
        return ""

    @check_deprecation
    def get_stderr(self) -> str:
        logs = self.get_logs_urls()
        if logs and logs.stdout_location_url:
            response = requests.get(logs.stderr_location_url)
            if response.status_code == 200:
                return response.text
        return ""


class JobRunLogsResponse(SDKBaseModel, IJobRunLogsResponse):
    """
    Represents the response object containing URLs for accessing logs related to a job run.

    Attributes:
        stderr_location_url (str): The URL to access the standard error logs of the job run.
        stdout_location_url (str): The URL to access the standard output logs of the job run.
        expiration_date (str): The date when the log URLs will expire and no longer be accessible.
    """

    stderr_location_url: str = Field(None, alias="stderrUrl")
    stdout_location_url: str = Field(None, alias="stdoutUrl")
    expiration_date: str = Field(None, alias="expirationDate")


class JobFilter(SDKBaseModel):
    """
    Provides filtering options for querying job-related data.

    Attributes:
        ids (Optional[List[Union[str, UUID]]]): A list of job IDs to filter by.
        template_ids (Optional[List[Union[str, UUID]]]): A list of job template IDs to filter by.
        cluster_ids (Optional[List[Union[str, UUID]]]): A list of cluster IDs to filter jobs by.
        types (Optional[List[str]]): A list of job types to filter by.
        statuses (Optional[List[str]]): A list of job statuses to filter by.
        started_at (Optional[datetime]): A datetime value to filter jobs that started after it.
        finished_at (Optional[datetime]): A datetime value to filter jobs that finished before it.
    """

    ids: Optional[List[Union[str, UUID]]] = None
    template_ids: Optional[List[Union[str, UUID]]] = None
    cluster_ids: Optional[List[Union[str, UUID]]] = None
    types: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class JobRunList(IJobRunList, SDKBaseModel):
    """
    Represents a paginated list of job runs, including metadata and filtering capabilities.

    Attributes:
        page (Optional[int]): The current page number in the paginated list. Defaults to 0.
        page_size (Optional[int]): The number of job runs to display per page. Defaults to 10.
        total (Optional[int]): The total number of job runs available.
        order (Optional[Dict]): A dictionary specifying the order in which job runs are sorted.
        filters (Optional[JobFilter]): A `JobFilter` object used to apply filtering on the list of job runs.
    """

    page: Optional[int] = Field(0, alias="page")
    page_size: Optional[int] = Field(10, alias="pageSize")
    total: Optional[int] = Field(None, alias="total")
    order: Optional[Dict] = Field(default_factory=dict, alias="order")
    filters: Optional[JobFilter] = None

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        """
        Initializes a new instance of JobRunList with optional parameters for
        configuration and a workspace client for API interactions.

        Args:
            workspace_client (IBodoWorkspaceClient, optional): The client used for workspace API calls.
                This client is responsible for fetching cluster data from the backend.
            **data: Arbitrary keyword arguments that can be used to set the values of the model fields
                upon initialization.
        """
        if "filters" in data and isinstance(data["filters"], dict):
            data["filters"] = JobFilter(**data["filters"])
        if data:
            super().__init__(**data)
        else:
            super().__init__()
        self._elements: List[IJobRun] = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> JobRunList:
        if "filters" in data and isinstance(data["filters"], dict):
            data["filters"] = JobFilter(**data["filters"])
        jobs = JobRunList(workspace_client=self._workspace_client, **data)
        return jobs._load_next_page()

    @check_deprecation
    def cancel(self) -> JobRunList:
        """
        Cancels all jobs in the list.

        This method iterates through each job in the current list (represented by instances of this class),
        and calls the `cancel` method on each job to attempt their cancellation.
        After attempting to cancel all jobs, it returns the updated list of jobs.

        Returns:
            JobRunList: The list instance, potentially with updated states of the individual jobs
            if the cancellation requests were successful.

        Note:
            This method relies on the individual `cancel()` method of the job objects within the list.
            If any job cancellation fails, it could raise an exception depending on
            the implementation of the individual `cancel()` method.

        """
        for job in self:
            job.cancel()
        return self

    def _load_next_page(self) -> JobRunList:
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._job_api.list_job_runs(
            page=self.page,
            size=self.page_size,
            uuids=self.filters.ids if self.filters else None,
            types=self.filters.types if self.filters else None,
            template_ids=self.filters.template_ids if self.filters else None,
            cluster_ids=self.filters.cluster_ids if self.filters else None,
            statuses=self.filters.statuses if self.filters else None,
            started_at=self.filters.started_at if self.filters else None,
            finished_at=self.filters.finished_at if self.filters else None,
        )
        for resp_obj in resp["data"]:
            resp_obj["config"]["source"] = resp_obj["config"]["source"]["sourceDef"]
            self._elements.append(self._workspace_client.JobClient.JobRun(**resp_obj))
        self.total = resp["metadata"]["total_items"]
        self._deprecated_fields.update(
            resp.get("_deprecatedFields")
            if isinstance(resp.get("_deprecatedFields"), dict)
            else {}
        )
        self._deprecated_methods.update(
            resp.get("_deprecatedMethods")
            if isinstance(resp.get("_deprecatedMethods"), dict)
            else {}
        )
        self._mutable = False
        return self

    @property
    def clusters(self):
        uuids = []
        for job in self:
            uuids.append(job.cluster.uuid)
        return self._workspace_client.ClusterClient.ClusterList(filters={"ids": uuids})

    @check_deprecation
    def wait_for_status(
        self, statuses: List[str], timeout: int = 3600, tick: int = 30
    ) -> JobRunList:
        """
        Waits for each job in the list to reach one of the specified statuses, polling each at regular intervals.

        This method iterates over each job within the list, checking at intervals (defined by `tick`) to see
        if the job has reached one of the desired statuses specified in `statuses`.
        If a job reaches the desired status within the `timeout` period, the method continues to the next job.
        If the timeout is reached without the job reaching the desired status, a `TimeoutException` is raised.

        Parameters:
            statuses (list or tuple): A list or tuple of statuses that each job is expected to reach.
            timeout (int, optional): The maximum time in seconds to wait for each job to reach one of
            the specified statuses. Defaults to 600 seconds.
            tick (int, optional): The time interval in seconds between status checks for each job.
            Defaults to 30 seconds.

        Returns:
            JobRunList: The job run list instance, after attempting to wait for all jobs to reach the desired statuses.

        Raises:
            TimeoutException: If any job does not reach one of the specified statuses within the specified
            timeout period, including details of the job's UUID and its current status.

        Decorators:
            @check_deprecation: Checks if the method or its parameters are deprecated.

        Note:
            This method individually tracks the timeout for each job, resetting the start time at the beginning
            of the wait for each job in the list.

        """
        for job in self:
            job.wait_for_status(statuses, timeout, tick)
        return self

    @check_deprecation
    def refresh(self) -> JobRunList:
        """
        Refreshes the list of jobs by clearing the current elements and reloading the next page of job data.

        This method resets the internal state of the list, including the pagination index and the elements themselves.
        It then loads the next page of data from the underlying data source to repopulate the list.
        The list is temporarily set to mutable during this process to allow updates, and then set back to immutable
        once the refresh is complete.

        Returns:
            JobRunList: The refreshed job run list instance, with elements reloaded from the next available page.

        Note:
            This method assumes that the list supports pagination and that the underlying data source provides
            the mechanism to load additional pages of data.

        """
        self._mutable = True
        self._index = 0
        self.page = 0
        self._elements = []
        self._load_next_page()
        self._mutable = False
        return self


class JobTemplateFilter(SDKBaseModel, IJobTemplateFilter):
    """
    Class representig filters for JobTemplateList

    Attributes:
        ids: returns list matching given ids
        names: returns list matching given names
        tags: returns list matching given tags
    """

    ids: Optional[List[str]] = Field(default_factory=list)
    names: Optional[List[str]] = Field(default_factory=list)
    tags: Optional[dict] = Field(default_factory=dict)


class JobTemplateList(IJobTemplateList, SDKBaseModel):
    """
    Represents a list of JobTemplates, providing pagination and filtering capabilities.

    Attributes:
        page (Optional[int]): The current page number in the list of Job Templates. Defaults to 0.
        page_size (Optional[int]): The number of Job Templates to display per page. Defaults to 10.
        total (Optional[int]): The total number of Job Templates available.
        order (Optional[Dict]): A dictionary specifying the order in which Job Templates are sorted.

        filters (Optional[InstanceRoleFilter]): A filter object used to filter the Job Templates listed.

    """

    _workspace_client: IBodoWorkspaceClient
    page: Optional[int] = Field(0, alias="page")
    page_size: Optional[int] = Field(10, alias="pageSize")
    total: Optional[int] = Field(None, alias="total")
    order: Optional[Dict] = Field(default_factory=dict, alias="order")
    filters: Optional[JobTemplateFilter] = None

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        if "filters" in data and isinstance(data["filters"], dict):
            data["filters"] = JobTemplateFilter(**data["filters"])
        super().__init__(**data)
        self._elements = []
        self._workspace_client = workspace_client

    def __call__(self, **data) -> "IJobTemplateList":
        if "filters" in data and isinstance(data["filters"], dict):
            data["filters"] = JobTemplateFilter(**data["filters"])
        job_defs = JobTemplateList(workspace_client=self._workspace_client, **data)
        return job_defs._load_next_page()

    @check_deprecation
    def delete(self):
        """
        Deletes all job definitions in the list.

        This method iterates over each job definition contained within the list and calls its individual
        `delete` method. This action attempts to remove each job definition from the underlying storage
        or management system.

        Note:
            The behavior and success of the deletion process depend on the implementation of the individual
            `delete` method of each job definition. This may include handling exceptions and ensuring that each
            job definition is properly removed. If an error occurs during the deletion of any job definition,
            it may raise an exception, which should be handled by the caller or within the individual `delete` methods.

        """
        for job_def in self:
            job_def.delete()

    @check_deprecation
    def run(
        self,
        instance_type: str = None,
        workers_quantity: int = None,
        bodo_version: str = None,
    ) -> IJobRunList:
        """)
        Executes all job definitions in the list with specified configurations and aggregates their run IDs.

        This method iterates over each job definition in the list and invokes the `run` method on each, passing
        the specified configuration parameters such as instance type, the quantity of workers, and the Bodo version.
        It collects the IDs of the resulting job runs and returns a consolidated list of these job runs.

        Parameters:
            instance_type (str, optional): The type of instance to use for the jobs.
            This may specify the hardware specifications.
            workers_quantity (int, optional): The number of worker instances to deploy for the jobs.
            bodo_version (str, optional): The specific version of Bodo to use for executing the jobs.

        Returns:
            IJobRunList: An interface to the list of job runs created by executing the job definitions,
            allowing further operations like monitoring and management.

        Note:
            The `run` method for each job definition must correctly handle the passed configurations.
            If any job execution fails, the behavior and handling of errors should be considered based
            on the implementation of each job definition's `run` method.

        """
        run_uuids = []
        for job_def in self:
            run = job_def.run(
                instance_type=instance_type,
                workers_quantity=workers_quantity,
                bodo_version=bodo_version,
            )
            run_uuids.append(run.id)
        return JobRunList(
            workspace_client=self._workspace_client, filters={"ids": run_uuids}
        )

    def _load_next_page(self) -> JobTemplateList:
        self._mutable = True
        self.page += 1
        resp = self._workspace_client._job_tpl_api.list_job_tpl(
            self.page,
            self.page_size,
            names=self.filters.names if self.filters else None,
            uuids=self.filters.ids if self.filters else None,
            tags=self.filters.tags if self.filters else None,
        )
        for resp_obj in resp["data"]:
            resp_obj["config"]["source"] = resp_obj["config"]["source"]["sourceDef"]
            self._elements.append(
                self._workspace_client.JobTemplateClient.JobTemplate(**resp_obj)
            )
        self._deprecated_fields.update(
            resp.get("_deprecatedFields")
            if isinstance(resp.get("_deprecatedFields"), dict)
            else {}
        )
        self._deprecated_methods.update(
            resp.get("_deprecatedMethods")
            if isinstance(resp.get("_deprecatedMethods"), dict)
            else {}
        )
        self.total = resp["metadata"]["total_items"]
        self._mutable = False
        return self

    @check_deprecation
    def refresh(self) -> JobTemplateList:
        """
        Refreshes the list of job templates by clearing the current elements and reloading the next page of job data.

        This method resets the internal state of the list, including the pagination index and the elements themselves.
        It then loads the next page of data from the underlying data source to repopulate the list.
        The list is temporarily set to mutable during this process to allow updates, and then set back to
        immutable once the refresh is complete.

        Returns:
            JobTemplateList: The refreshed job template list instance, with elements reloaded from
            the next available page.

        Note:
            This method assumes that the list supports pagination and that the underlying data source provides
            the mechanism to load additional pages of data.

        """
        self._mutable = True
        self._index = 0
        self.page = 0
        self._elements = []
        self._load_next_page()
        self._mutable = False
        return self


class JobTemplate(SDKBaseModel, IJobTemplate):
    """
    Represents a template for creating and managing jobs within an SDK environment, e
    ncapsulating common job configurations.

    Attributes:
        uuid (Optional[str]): The unique identifier for the job template.
        name (Optional[str]): The name of the job template.
        job_runs (List[JobRun]): A list of job runs associated with this template. Default is an empty list
        if none are specified.
        description (Optional[str]): A brief description of the job template.
        created_by (Optional[str]): The identifier of the user who created the job template.
        config (Optional[JobConfig]): The job configuration specifics for this template.
        cluster_config (Optional[Cluster]): Configuration details of the cluster on which the jobs will run. D
        efault is None.

    """

    _workspace_client = None
    uuid: Optional[str]
    name: Optional[str]
    job_runs: List[JobRun] = Field(None, alias="jobRuns")
    description: Optional[str]
    created_by: Optional[str] = Field(None, alias="createdBy")
    config: Optional[JobConfig]
    cluster_config: Optional["Cluster"] = Field(None, alias="clusterConfig")

    @property
    def id(self):
        return self.uuid

    def __init__(self, workspace_client: IBodoWorkspaceClient = None, **data):
        super().__init__(**data)
        self._workspace_client = workspace_client

    def __call__(self, **data) -> JobTemplate:
        return JobTemplate(self._workspace_client, **data)

    @check_deprecation
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
    ):
        return self._workspace_client.JobClient.run(
            template_id=self.uuid,
            cluster=cluster,
            name=name,
            code_type=code_type,
            source=source,
            exec_file=exec_file,
            exec_text=exec_text,
            args=args,
            env_vars=env_vars,
            timeout=timeout,
            num_retries=num_retries,
            delay_between_retries=delay_between_retries,
            retry_on_timeout=retry_on_timeout,
            catalog=catalog,
        )

    @check_deprecation
    def delete(self):
        self._workspace_client._job_tpl_api.delete_job_tpl(self.uuid)

    @check_deprecation
    def _save(self) -> JobTemplate:
        if self._modified:
            if not self.uuid:
                resp = self._workspace_client._job_tpl_api.create_job_tpl(self)

            else:
                resp = self._workspace_client._job_tpl_api.update_job_tpl(self)
            self._update(resp)
            self._modified = False
        return self

    @check_deprecation
    def _load(self) -> JobTemplate:
        resp = self._workspace_client._job_tpl_api.get_job_tpl(self.uuid)
        if resp.get("config", {}).get("source", {}).get("sourceDef"):
            resp["config"]["source"] = resp["config"]["source"]["sourceDef"]
        self._update(resp)
        return self


from bodosdk.models import Cluster  # noqa

JobRun.update_forward_refs()
JobTemplate.update_forward_refs()
