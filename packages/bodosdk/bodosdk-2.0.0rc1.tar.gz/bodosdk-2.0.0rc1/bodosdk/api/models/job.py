import enum
from datetime import date, datetime
from typing import Optional, Dict, Union, List
from uuid import UUID

import pydantic
from pydantic import Field

from bodosdk.api.models import ClusterResponse, ClusterDefinition
from bodosdk.base import APIBaseModel, PaginationOrder


class JobClusterDefinition(APIBaseModel):
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    accelerated_networking: bool = Field(..., alias="acceleratedNetworking")
    image_id: Optional[str] = Field(None, alias="imageId")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    instance_role_uuid: Optional[str] = Field(None, alias="instanceRoleUUID")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    aws_deployment_subnet_id: Optional[str] = Field(None, alias="awsDeploymentSubnetId")
    custom_tags: Optional[Dict[str, str]] = Field(None, alias="customTags")
    auto_pause: Optional[int] = Field(60, alias="autoPause")
    auto_stop: Optional[int] = Field(0, alias="autoStop")


class JobCluster(pydantic.BaseModel):
    uuid: Union[str, UUID]


class JobSourceType(enum.Enum):
    GIT = "GIT"
    S3 = "S3"
    WORKSPACE = "WORKSPACE"
    SQL = "SQL"

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)


class GitRepoSource(APIBaseModel):
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

    type: JobSourceType = Field(JobSourceType.GIT, const=True)
    repo_url: str = Field(..., alias="repoUrl")
    reference: Optional[str] = ""
    username: str
    token: str


class S3Source(APIBaseModel):
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

    type: JobSourceType = Field(JobSourceType.S3, const=True)
    bucket_path: str = Field(..., alias="bucketPath")
    bucket_region: str = Field(..., alias="bucketRegion")


class WorkspaceSource(pydantic.BaseModel):
    """
    WorkspaceAPIModel source definition.

    ...

    Attributes
    ----------
    path: str
        WorkspaceAPIModel path.
    """

    type: JobSourceType = Field(JobSourceType.WORKSPACE, const=True)
    path: str


class SQLSource(APIBaseModel):
    """
    SQL source definition.

    ...
    """

    type: JobSourceType = Field(JobSourceType.SQL, const=True)


class JobRunLogsResponseApiModel(APIBaseModel):
    stderr_location_url: str = Field(None, alias="stderrUrl")
    stdout_location_url: str = Field(None, alias="stdoutUrl")
    expiration_date: str = Field(None, alias="expirationDate")


class JobSource(APIBaseModel):
    """
    Job source.

    ...

    Attributes
    ----------
    type: JobSourceType
        Job source type.

    definition: Union[GitDef, S3Def, WorkspaceDef]
        Job source definition.
    """

    type: JobSourceType
    definition: Union[GitRepoSource, S3Source, WorkspaceSource, SQLSource] = Field(
        ..., alias="sourceDef"
    )


class RetryStrategy(APIBaseModel):
    """
    Retry strategy for a job.

    ...

    Attributes
    ----------
    num_retries: int
        Number of retries for a job. (Default: 0)

    delay_between_retries: int
        Delay between retries in minutes. (Default: 1)

    retry_on_timeout: bool
        Retry on timeout. (Default: False)

    """

    num_retries: int = Field(0, alias="numRetries")
    delay_between_retries: int = Field(1, alias="delayBetweenRetries")  # in minutes
    retry_on_timeout: bool = Field(False, alias="retryOnTimeout")


class SourceCodeType(enum.Enum):
    PYTHON = "PYTHON"
    IPYNB = "IPYNB"
    SQL = "SQL"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class JobConfig(APIBaseModel):
    """
    Job configuration.

    ...

    Attributes
    ----------
    source: JobSource
        Job source.

    source_code_type: SourceCodeType
        Job source code type.

    source_location: Optional[str]
        Job source location.

    args: Union[str, Dict]
        Job arguments. (Default: {})

    retry_strategy: Optional[RetryStrategy]
        Job retry strategy.
        (Default: {num_retries: 0, delay_between_retries: 1, retry_on_timeout: False})

    timeout: int
        Job timeout in minutes. (Default: 60)

    env_vars: Dict
        Job environment variables. (Default: {})

    catalog: Optional[str]
        Catalog name. (Default: None)

    """

    type: Optional[str]
    source: Optional[JobSource]
    exec_file: Optional[str] = Field(None, alias="sourceLocation")
    exec_text: Optional[str] = Field(None, alias="sqlQueryText")
    sql_query_parameters: Optional[dict] = Field(None, alias="sqlQueryParameters")
    args: Optional[Union[dict, str]]
    retry_strategy: Optional[RetryStrategy] = Field(None, alias="retryStrategy")
    timeout: Optional[int]
    env_vars: Optional[dict] = Field(None, alias="envVars")
    catalog: Optional[str]

    def __repr__(self):
        repr_str = ""
        for k, v in self.dict().items():
            if v is not None:
                repr_str += f"{k}: {v}\n"
            else:
                repr_str += f"{k}: None\n"
        return repr_str[:-1]  # remove last newline

    def __str__(self):
        return self.__repr__()


class CreateBatchJobDefinition(APIBaseModel):
    """
    Batch job definition.

    ...

    Attributes
    ----------
    description: str
        Job definition description.

    config: JobConfig
        Job configuration.

    cluster_config: JobClusterDefinition
        Job cluster configuration.

    """

    name: str
    description: str
    config: JobConfig
    cluster_config: Optional[JobClusterDefinition] = Field(
        default=None, alias="clusterConfig"
    )
    tags: Optional[dict] = Field(default_factory=dict)


class JobRunPriceExportResponse(APIBaseModel):
    """
    Job run price export response

    ...

    Attributes
    ----------
    url: str
        String to S3 bucket with the price export data
    """

    url: str


class JobRunPricingResponse(APIBaseModel):
    """
    Represents a response object for job run pricing information.

    Attributes:
    name (str): The name of the job.
    jobRunUUID (str): The UUID of the job run.
    batchJobDefinitionUUID (str): The UUID of the batch job definition.
    clusterWorkersQuantity (int): The quantity of cluster workers.
    clusterInstanceType (str): The instance type of the cluster.
    clusterName (str): The name of the cluster.
    sqlQuery (str): The SQL query executed by the job.
    clusterUseSpotInstance (bool): Indicates whether the cluster uses spot instances.
    startedAt (date): The start date of the job run.
    inishedAt (date): The end date of the job run.
    status (str): The status of the job run.
    duration (float): The duration of the job run in seconds.
    instancePrice (float): The price per instance.
    bodoHourlyRate (float): The hourly rate for using Bodo.
    totalAWSPrice (float): The total price charged by AWS.
    totalBodoPrice (float): The total price charged by Bodo.
    """

    name: str
    job_run_uuid: str = Field(..., alias="jobRunUUID")
    batch_job_definition_uuid: str = Field(..., alias="batchJobDefinitionUUID")
    cluster_workers_quantity: int = Field(..., alias="clusterWorkersQuantity")
    cluster_instance_type: str = Field(..., alias="clusterInstanceType")
    cluster_name: str = Field(..., alias="clusterName")
    sql_query: str = Field(..., alias="sqlQuery")
    cluster_use_spot_instance: bool = Field(..., alias="clusterUseSpotInstance")
    started_at: date = Field(..., alias="startedAt")
    finished_at: date = Field(..., alias="finishedAt")
    status: str
    duration: float
    instance_price: float = Field(..., alias="instancePrice")
    bodo_hourly_rate: float = Field(..., alias="bodoHourlyRate")
    total_aws_price: float = Field(..., alias="totalAWSPrice")
    total_bodo_price: float = Field(..., alias="totalBodoPrice")


DEFAULT_PAGE_SIZE = 5
DEFAULT_PAGE = 1
DEFAULT_ORDER = PaginationOrder.ASC

LIST_QUERY_PARAMS = [
    "type",
    "jobTemplateUUID",
    "status",
    "clusterUUID",
    "startedAt",
    "finishedAt",
    "page",
    "size",
    "order",
]


class JobRunApiModel(APIBaseModel):
    uuid: Optional[str]
    name: Optional[str]
    type: Optional[str] = "BATCH"
    submitted_at: Optional[datetime] = Field(None, alias="submittedAt")
    finished_at: Optional[datetime] = Field(None, alias="finishedAt")
    last_health_check: Optional[datetime] = Field(None, alias="lastHealthCheck")
    last_known_activity: Optional[datetime] = Field(None, alias="lastKnownActivity")
    status: Optional[str]
    reason: Optional[str]
    num_retries_used: Optional[int] = (Field(None, alias="numRetriesUsed"),)
    tags: Optional[List] = Field(default_factory=list, alias="tag")
    cluster_id: Optional[str] = Field(None, alias="clusterUUID")
    cluster: Optional[ClusterResponse]
    cluster_config: Optional[ClusterDefinition] = Field(None, alias="clusterConfig")
    config: Optional[Union[JobConfig]] = Field(None, alias="jobConfig")
    job_template_id: Optional[str] = Field(None, alias="jobTemplateUUID")
    submitter: Optional[str]
    stats: Optional[dict]


class JobTplApiModel(APIBaseModel):
    uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    config: Optional[JobConfig]
    cluster_config: Optional[ClusterDefinition] = Field(None, alias="clusterConfig")
    tags: Optional[dict]
