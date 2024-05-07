from typing import Optional, Union, Dict, List

from bodosdk import _version
from bodosdk.db.connection import Connection
from bodosdk.interfaces import IBodoWorkspaceClient, IClusterClient, IBodoImage
from bodosdk.deprecation_decorator import check_deprecation
from bodosdk.models.cluster import Cluster, ClusterList, ClusterFilter, InstanceType
from bodosdk.models.instance_role import InstanceRole


class ClusterClient(IClusterClient):
    """
    A client for managing cluster operations in a Bodo workspace.

    Attributes:
       _deprecated_methods (Dict): A dictionary of deprecated methods.
       _images (List[IBodoImage]): A list of available Bodo images.

    Args:
       workspace_client (IBodoWorkspaceClient): The workspace client used for operations.
    """

    _deprecated_methods: Dict
    _images: List[IBodoImage]

    def __init__(self, workspace_client: IBodoWorkspaceClient):
        """
        Initializes the ClusterClient with a given workspace client.

        Args:
            workspace_client (IBodoWorkspaceClient): The workspace client to interact with the API.
        """
        self._workspace_client = workspace_client
        self._check_deprecation()
        self._images = []

    def _check_deprecation(self):
        """
        Checks for any deprecated methods and updates the _deprecated_methods attribute accordingly.
        """
        methods = self._workspace_client._sdk_api.get_cluster_client_info(
            _version.get_versions().get("version")
        )
        if isinstance(methods, dict) and methods:
            self._deprecated_methods = methods
        else:
            self._deprecated_methods = {}

    @property
    def Cluster(self) -> Cluster:
        """
        Provides access to cluster operations.

        Returns:
            Cluster: An instance of Cluster for cluster operations.
        """
        return Cluster(self._workspace_client)

    @property
    def ClusterList(self) -> ClusterList:
        """
        Provides access to listing clusters.

        Returns:
            ClusterList: An instance of ClusterListAPIModel for listing clusters.
        """
        return ClusterList(self._workspace_client)

    @check_deprecation
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
        instance_role: Optional[Union[InstanceRole, Dict]] = None,
        custom_tags: Optional[Dict] = None,
    ) -> Cluster:
        """
        Creates a new cluster with the specified configuration.

        Args:
            name (str): The name of the cluster.
            instance_type (str, optional): The type of instance to use for the cluster nodes.
            workers_quantity (int, optional): The number of worker nodes in the cluster.
            description (str, optional): A description of the cluster.
            bodo_version (str, optional): The Bodo version to use for the cluster.
            auto_stop (int, optional): The auto-stop time in minutes for the cluster.
            auto_pause (int, optional): The auto-pause time in minutes for the cluster.
            image_id (str, optional): The ID of the image to use for the cluster.
            accelerated_networking (bool, optional): Whether to use accelerated networking.
            auto_az (bool, optional): Whether to automatically select the availability zone.
            use_spot_instance (bool, optional): Whether to use spot instances for the cluster.
            aws_deployment_subnet_id (str, optional): The AWS deployment subnet ID.
            availability_zone (str, optional): The availability zone for the cluster.
            instance_role (InstanceRole | Dict, optional): The instance role or a custom role configuration.
            custom_tags (Dict, optional): Custom tags to assign to the cluster resources.

        Returns:
            Cluster: The created Cluster object.
        """
        local_vars = locals().copy()
        local_vars.pop("self", None)
        cleaned_dict = {k: v for k, v in local_vars.items() if v is not None}
        cluster = self.Cluster()._update(cleaned_dict)
        return cluster._save()

    @check_deprecation
    def get(self, id: str) -> Cluster:
        """
        Retrieves a cluster by its ID.

        Args:
            id (str): The ID of the cluster to retrieve.

        Returns:
            Cluster: The retrieved Cluster object.
        """
        return self.Cluster(uuid=id)._load()

    @check_deprecation
    def list(
        self,
        filters: Optional[Union[Dict, ClusterFilter]] = None,
        order: Optional[Dict] = None,
    ) -> ClusterList:
        """
        Lists clusters based on the provided filters and order.

        Args:
            filters (Dict | ClusterFilter, optional): The filters to apply to the cluster listing.
            order (Dict, optional): The order in which to list the clusters.

        Returns:
            ClusterList: A list of clusters matching the criteria.
        """
        return self.ClusterList(filters=filters, order=order)

    @check_deprecation
    def pause(self, id: str, wait=False) -> Cluster:
        """
        Pauses the specified cluster.

        Args:
            id (str): The ID of the cluster to pause.

        Returns:
            Cluster: The paused Cluster object.
        """
        return self.Cluster(uuid=id)._load().pause(wait)

    @check_deprecation
    def resume(self, id: str, wait=False) -> Cluster:
        """
        Resumes the specified paused cluster.

        Args:
            id (str): The ID of the cluster to resume.

        Returns:
            Cluster: The resumed Cluster object.
        """

        return self.Cluster(uuid=id)._load().resume(wait)

    @check_deprecation
    def stop(self, id: str, wait=False) -> Cluster:
        """
        Stops the specified cluster.

        Args:
            id (str): The ID of the cluster to stop.

        Returns:
            Cluster: The stopped Cluster object.
        """

        return self.Cluster(uuid=id)._load().stop(wait)

    @check_deprecation
    def start(self, id: str, wait=False) -> Cluster:
        """
        Starts the specified stopped cluster.

        Args:
            id (str): The ID of the cluster to start.

        Returns:
            Cluster: The started Cluster object.
        """

        return self.Cluster(uuid=id)._load().start(wait)

    @check_deprecation
    def remove(self, id: str, wait=False) -> Cluster:
        """
        Removes the specified cluster.

        Args:
            id (str): The ID of the cluster to remove.

        Returns:
            None
        """

        return self.Cluster(uuid=id).delete(wait=wait)

    @check_deprecation
    def update(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        auto_stop: Optional[int] = None,
        auto_pause: Optional[int] = None,
        workers_quantity: Optional[int] = None,
        instance_role: Optional[Union[InstanceRole, Dict]] = None,
        instance_type: Optional[str] = None,
        bodo_version: Optional[str] = None,
        auto_az: Optional[bool] = None,
        availability_zone: Optional[str] = None,
        custom_tags: Optional[Dict] = None,
    ) -> Cluster:
        """
        Updates the specified cluster with the given configuration.

        Args:
            id (str): The ID of the cluster to update.
            name (str, optional): The new name for the cluster.
            description (str, optional): A new description for the cluster.
            auto_stop (int, optional): The new auto-stop time in minutes.
            auto_pause (int, optional): The new auto-pause time in minutes.
            workers_quantity (int, optional): The new number of worker nodes.
            instance_role (InstanceRole | Dict, optional): The new instance role or custom role configuration.
            instance_type (str, optional): The new instance type for the cluster nodes.
            bodo_version (str, optional): The new Bodo version for the cluster.
            auto_az (bool, optional): Whether to automatically select the availability zone.
            availability_zone (str, optional): The new availability zone for the cluster.
            custom_tags (Dict, optional): New custom tags for the cluster resources.

        Returns:
            Cluster: The updated Cluster object.
        """
        local_vars = locals().copy()
        local_vars.pop("self", None)
        cleaned_dict = {k: v for k, v in local_vars.items() if v is not None}
        return self.Cluster(uuid=id, **cleaned_dict)._save()

    @check_deprecation
    def scale(self, id: str, new_size: int) -> Cluster:
        """
        Scales the specified cluster to the new size.

        Args:
            id (str): The ID of the cluster to scale.
            new_size (int): The new size for the cluster in terms of the number of worker nodes.

        Returns:
            Cluster: The scaled Cluster object.
        """
        return self.Cluster(uuid=id).update(workers_quantity=new_size)

    @check_deprecation
    def wait_for_status(
        self,
        id: str,
        statuses: List,
        timeout: Optional[int] = 300,
        tick: Optional[int] = 30,
    ) -> Cluster:
        """
        Waits for the specified cluster to reach any of the given statuses within the timeout period.

        Args:
            id (str): The ID of the cluster to monitor.
            statuses (List): The list of statuses to wait for.
            timeout (int, optional): The timeout period in seconds.
            tick (int, optional): The interval in seconds between status checks.

        Returns:
            Cluster: The Cluster object if it reaches the desired status within the timeout period.
        """
        return self.Cluster(uuid=id).wait_for_status(statuses, timeout, tick)

    @check_deprecation
    def get_bodo_versions(self) -> List[str]:
        """
        Retrieves a list of available Bodo versions.

        Returns:
            List[str]: A list of available Bodo versions.
        """
        if not self._images:
            self._images = self._workspace_client._workspace_api.available_images(
                self._workspace_client._workspace_uuid
            )
        return [i.bodo_version for i in self._images]

    @check_deprecation
    def get_images(self) -> List[str]:
        """
        Retrieves a list of available images.

        Returns:
            List[str]: A list of image IDs available for clusters.
        """
        if not self._images:
            self._images = self._workspace_client._workspace_api.available_images(
                self._workspace_client._workspace_uuid
            )
        return [i.image_id for i in self._images]

    @check_deprecation
    def get_instance_types(self) -> List[InstanceType]:
        """
        Retrieves list of all supported instance types

        Return:
            List[InstanceType]
        """
        return self._workspace_client._workspace_api.available_instances(
            self._workspace_client._workspace_uuid
        )

    @property
    def latest_bodo_version(self) -> str:
        """
        Retrieves the latest Bodo version available.

        Returns:
            str: The latest Bodo version.
        """
        if not self._images:
            self._images = self._workspace_client._workspace_api.available_images(
                self._workspace_client._workspace_uuid
            )
        return self._images[0].bodo_version

    @check_deprecation
    def connect(self, catalog: str, cluster_id: str) -> Connection:
        cluster = self.Cluster(uuid=cluster_id)
        return Connection(catalog, cluster)
