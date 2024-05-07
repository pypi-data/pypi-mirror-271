from bodosdk.interfaces import ICluster, IJobRun


class QueryError(Exception):
    pass


class Cursor:
    def __init__(self, catalog: str, cluster: ICluster, timeout: int):
        self._catalog = catalog
        self.cluster = cluster
        self._timeout = timeout
        self._job: IJobRun = None

    def execute(self, query: str, **kwargs):
        self._job = self.cluster.run_sql_query(
            catalog=self._catalog, sql_query=query, args=kwargs, timeout=self._timeout
        )
        self._wait_for_finished_job()
        return self

    def execute_async(self, query: str, **kwargs):
        self._job = self.cluster.run_sql_query(
            catalog=self._catalog, sql_query=query, args=kwargs
        )
        return self

    def fetchone(self):
        self._wait_for_finished_job()
        return ("Query run successfully",)

    def fetchmany(self, size):
        self._wait_for_finished_job()
        # TODO: return part of result
        return ("Query run successfully",)

    def fetchall(self):
        self._wait_for_finished_job()
        return ("Query run successfully",)

    def _wait_for_finished_job(self):
        self._job.wait_for_status(
            ["SUCCEEDED", "FAILED", "CANCELLED"], tick=10, timeout=self._timeout
        )
        if self._job.status in ["FAILED", "CANCELLED"]:
            raise QueryError(f"Query failed due to {self._job.reason}")


class Connection:
    def __init__(self, catalog: str, cluster: ICluster, timeout=3600):
        self._catalog = catalog
        self._cluster = cluster
        self._timeout = timeout

    def cursor(self):
        return Cursor(self._catalog, self._cluster, self._timeout)
