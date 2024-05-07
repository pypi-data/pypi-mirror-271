# Bodo Platform SDK

Bodo Platform SDK is a Python library that provides a simple way to interact with the Bodo Platform API. It allows you
to create, manage, and monitor resources such as clusters, jobs, and workspaces.

## Getting Started

### Installation

```shell
pip install bodosdk
```

### Creating workspace client

First you need to access your workspace in `https://platform.bodo.ai/` and create an _API Token_ in the Bodo Platform
for
Bodo SDK authentication.

Navigate to _API Tokens_ in the Admin Console to generate a token.
Copy and save the token's _Client ID_ and _Secret Key_ and use them to define a client (`BodoClient`) that can interact
with the Bodo Platform.

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient(
    client_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    secret_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

Alternatively, set `BODO_CLIENT_ID` and `BODO_SECRET_KEY` environment variables
to avoid requiring keys:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
```

To get workspace data, you can access the `workspace_data` attribute of the client:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
print(my_workspace.workspace_data)
```

### Additional Configuration Options for `BodoClient`

- `print_logs`: defaults to False. All API requests and responses are printed to the console if set to True.

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient(print_logs=True)
```

### Create first cluster

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.create(
    name='My first cluster',
    instance_type='c5.large',
    workers_quantity=1
)
```

Above example creates a simple one node cluster, with latest bodo version available and returns cluster object.
Platform will create cluster in your workspace.

### Waiting for status

To wait till cluster will be ready for interaction you can call
method `wait_for_status`

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.create(
    name='My first cluster',
    instance_type='c5.large',
    workers_quantity=1
)
my_cluster.wait_for_status(['RUNNING'])
```

This method will wait until any of provided statuses will occur or `FAILED` status will be set in case of some failure.
Check your workspace on `https://platform.bodo.ai/` and you will see your cluster, you can use Notebook to connect with
it.

### Updating Cluster

Now let's update our cluster, on `RUNNING` cluster you can update `name`, `description`, `auto_pause`, `auto_stop`
and `workers_quantity`(this will trigger scaling) only:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.create(
    name='My first cluster',
    instance_type='c5.large',
    workers_quantity=1
)
my_cluster.wait_for_status(['RUNNING'])
my_cluster.update(
    description='My description',
    name="My updated cluster",
    auto_pause=15,
    auto_stop=30
)
```

All other modifcations like `instance_type`, `bodo_version` etc need `STOPPED` cluster

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.get("cluster_id")
if my_cluster.status != 'STOPPED':
    my_cluster.stop(wait=True)
my_cluster.update(instance_type='c5.2xlarge', workers_quantity=2)
```

### Create Fisrst Job

On running cluster you can schedule a job in very simple way:
First on `https://platform.bodo.ai` navigate to notebook in your workspace and
create following `test.py` file in your main directory:

```python
import pandas as pd
import numpy as np
import bodo
import time

NUM_GROUPS = 30
NUM_ROWS = 20_000_000

df = pd.DataFrame({
    "A": np.arange(NUM_ROWS) % NUM_GROUPS,
    "B": np.arange(NUM_ROWS)
})
df.to_parquet("my_data.pq")
time.sleep(1) # wait till file will be available on all nodes
@bodo.jit(cache=True)
def computation():
    t1 = time.time()
    df = pd.read_parquet("my_data.pq")
    df1 = df[df.B > 4].A.sum()
    print("Execution time:", time.time() - t1)
    return df1

result = computation()
print(result)
```

then define job on cluster through SDK, wait till `SUCCEEDED` and check logs

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.get("cluster_id")
my_job = my_cluster.run_job(
    code_type='PYTHON',
    source={'type': 'WORKSPACE', 'path': '/'},
    exec_file='test.py'
)
print(my_job.wait_for_status(['SUCCEEDED']).get_stdout())
```

You can use almost same confiuration to run SQL file, all you need is to define your `test.sql` file and Catalog `https://platform.bodo.ai`:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.get("cluster_id")
my_job = my_cluster.run_job(
    code_type='SQL',
    source={'type': 'WORKSPACE', 'path': '/'},
    exec_file='test.sql',
    catalog="MyCatalog"
)
print(my_job.wait_for_status(['SUCCEEDED']).get_stdout())

```

### Cluster List and executing jobs on it's elements

Now let's try to run same job on different clusters:

```python
from bodosdk import BodoWorkspaceClient
import random

my_workspace = BodoWorkspaceClient()

random_val = random.random() # just to avoid conflicts on name
clusters_conf = [('c5.large', 8), ('c5.xlarge',4), ('c5.2xlarge',2)]
for  i, conf in enumerate(clusters_conf):
    my_workspace.ClusterClient.create(
        name=f'Test {i}',
        instance_type=conf[0],
        workers_quantity=conf[1],
        custom_tags={'test_tag': f'perf_test{random_val}'} # let's add tag to easy filter our clusters
    )
# get list by tag
clusters = my_workspace.ClusterClient.list(filters={
    'tags': {'test_tag': f'perf_test{random_val}'}
})
# run same job 3 times, once per each cluster
jobs = clusters.run_job(
    code_type='PYTHON',
    source={'type': 'WORKSPACE', 'path': '/'},
    exec_file='test.py'
)
#wait for jobs to finish and print results
for job in jobs.wait_for_status(['SUCCEEDED']):
    print(job.name, job.cluster.name)
    print(job.get_stdout())
#remove our clusters
jobs.clusters.delete() # or clusters.delete()
```

### Execute SQL query

You can also execute SQL queries by passing just query text like following:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_sql_job = my_workspace.JobClient.run_sql_query(sql_query="SELECT 1", catalog="MyCatalog", cluster={
    "name": 'Temporary cluster',
    "instance_type": 'c5.large',
    "workers_quantity": 1
})
print(my_sql_job.wait_for_status(['SUCCEEDED']).get_stdout())
```

In above case, when you provide cluster configuration but not existing cluster it will be terminated as soon
as SQL job will finish.

If you want to execute sql job on existing cluster just use `run_sql_query` on cluster:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.create(
    name='My cluster',
    instance_type='c5.large',
    workers_quantity=1
)
my_sql_job = my_cluster.run_sql_query(sql_query="SELECT 1", catalog="MyCatalog")
print(my_sql_job.wait_for_status(['SUCCEEDED']).get_stdout())
```

### Connector

You can also execute SQL queries using connector for cluster:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.create(
    name='My cluster',
    instance_type='c5.large',
    workers_quantity=1
)
connection = my_cluster.connect('MyCatalog') # or connection = my_workspace.ClusterClient.connect('MyCatalog', 'cluster_id')
print(connection.cursor().execute("SELECT 1").fetchone())
my_cluster.delete()
```

### Job Templates

Against defining jobs from scratch you can create a template for your jobs, and then easily run them, e.g.:

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
tpl = my_workspace.JobTemplateClient.create(
    name='My template',
    cluster={
        'instance_type': 'c5.xlarge',
        'workers_quantity': 1
    },
    code_type="SQL",
    catalog="MyCatalog",
    exec_text="SELECT 1"
)
job1 = tpl.run() # you can simply run it
job2 = tpl.run(exec_text="SELECT 2") # or run it with overriding template values
job3 = tpl.run(cluster={'instance_type': 'c5.large'}) # you can override even part of cluster configuration

jobs = my_workspace.JobClient.list(filters={'template_ids':[tpl.id]}) # you can filter jobs by it's template_id
for job in jobs.wait_for_status(['SUCCEEDED']):
    print(job.name, job.cluster.instance_type, job.get_stdout())

```

You can also run your template on specific cluster e.g:

```python
from bodosdk import BodoWorkspaceClient
from bodosdk.models import JobTemplateFilter

my_workspace = BodoWorkspaceClient()
tpls = my_workspace.JobTemplateClient.list(filters=JobTemplateFilter(names=['My template']))
my_cluster = my_workspace.ClusterClient.create(
    name='My cluster',
    instance_type='c5.large',
    workers_quantity=1
)
print(my_cluster.run_job(template_id=tpls[0].id).wait_for_status(['SUCCEEDED']).get_stdout())
my_cluster.delete()
```

## Statuses

Each resource, Cluster, Job or Workspace has own set of statuses which are following:

### Cluster:

- NEW
- INPROGRESS
- PAUSING
- PAUSED
- STOPPING
- STOPPED
- INITIALIZING
- RUNNING
- FAILED
- TERMINATED

### Job:

- PENDING
- RUNNING
- SUCCEEDED
- FAILED
- CANCELLED
- CANCELLING
- TIMEOUT

### Workspace:

- NEW
- INPROGRESS
- READY
- FAILED
- TERMINATING
- TERMINATED

## Organization client and workspaces:

To manage workspaces you need different keys (generated for organization) and differenct SDK client, for start let's list
all our workspaces:

```python
from bodosdk import BodoOrganizationClient

my_org = BodoOrganizationClient(
    client_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    secret_key="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
) # or BodoOrganizationClient() if `BODO_ORG_CLIENT_ID` and `BODO_ORG_SECRET_KEY` are exported
for w in my_org.list_workspaces():
    print(w.name)
```

You can filter workspaces providing valid filters:

```python
from bodosdk import BodoOrganizationClient
from bodosdk.models import WorkspaceFilter
my_org = BodoOrganizationClient()

for w in my_org.list_workspaces(filters=WorkspaceFilter(statuses=['READY'])):
    print(w.name)
```

You can provide filters as 'WorkspaceFilter' imported from `bodosdk.models` or as a dictionary:

```python
from bodosdk import BodoOrganizationClient
my_org = BodoOrganizationClient()

for w in my_org.list_workspaces(filters={"statuses": ['READY']}):
    print(w.name)
```

### Create new Workspace

```python
from bodosdk import BodoOrganizationClient
my_org = BodoOrganizationClient()
my_workspace = my_org.create_workspace(
    name="SDK test",
    region='us-east-2',
    cloud_config_id="a0d1242c-3091-42de-94d9-548e2ae33b73",
    storage_endpoint_enabled=True
).wait_for_status(['READY'])
assert my_workspace.id == my_org.list_workspaces(filters={"names": ['SDK test'], "statuses": ['READY']})[0].id
my_workspace.delete() # remove workspace at the end
```

### Upgrade workspace infra

In some cases when you have workspace existing for a long time you may want to re-run terraform to
apply fresh changes to workspace infrastructure. You can do it following way:

```python
from bodosdk import BodoOrganizationClient
my_org = BodoOrganizationClient()
my_org.list_workspaces(filters={'ids': ['workspace_to_update1_id', 'workspace_to_update2_id']}).update_infra()
```

# Advanced

In this section we will present more examples of bodosdk usages.

## Workspace created in existing VPC

There is possibility to create workspace on existing infrastructure. The only requirement is that VPC need access to
Internet, either NAT or IGW. It's needed to allow clusters to authorize in external auth service.

```python
from bodosdk import BodoOrganizationClient
my_org = BodoOrganizationClient()
my_workspace = my_org.create_workspace(
    cloud_config_id="cloudConfigId",
    name="My workspace",
    region="us-east-1",
    storage_endpoint_enabled=True,
    vpc_id="existing-vpc-id",
    private_subnets_ids=['subnet1', 'subnet2'],
    public_subnets_ids=['subnet3']
)
my_workspace.wait_for_status(['READY'])
```

## Spot instances, auto AZ

You can create Cluster using spot instances, to reduce cost of usage, downside is that you cannot PAUSE
this kind of cluster, and from time to time cluster may be unavailable (when spot instance is released).

Auto AZ is mechanism which retries cluster creation in another AZ, when in current AZ
there is no enough instances of desired type.

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.create(
    name='Spot cluster',
    instance_type='c5.large',
    workers_quantity=1,
    use_spot_instance=True,
    auto_az=True,
)
```

## Accelerated networking

Accelerated networking set to True enables EFA for instances (raises error when instance type does not support)

You can get list of all supported instances using ClusterClient, it returns list of
InstanceType objects. For AWS field `efa` informs about network acceleration. For Azure it's
`network_acceleration` field.

```python
from bodosdk import BodoWorkspaceClient

my_workspace = BodoWorkspaceClient()

efa_supported_instances = [x for x in my_workspace.ClusterClient.get_instances() if x.efa]

my_cluster = my_workspace.ClusterClient.create(
    name='Spot cluster',
    instance_type=efa_supported_instances[0].name,
    workers_quantity=1,
    accelerated_networking=True
)
```

## Preparing clusters for future use:

In Bodo, Cluster may be in two states responsible for suspended status: `PAUSED` and `STOPPED`.
Spot clusters cannot be `PAUSED`. There are 3 differences between those states: cost, start up time, error rate.

### Costs

`PAUSED` > `STOPPED` - In `PAUSED` state we are paying for disks while in `STOPPED` we don't.

### Start up time

`STOPPED` > `PAUSED` - Bringing back machines in `PAUSED` state is much faster, as those machines are already
defined in cloud

### Error rate

`PAUSED` > `STOPPED` - By error rate we mean situation when number of available instances of descired types is lower
than number of requested workers. As in `PAUSED` state, instance entities are already defined,
and we request for reesources at once it's more likely to happen than in `STOPPED` state,
where asg is maintaining instance creation and it waits for available resources.

Prepare clusters for further use and make them `PAUSED`

```python
from bodosdk import BodoWorkspaceClient
from bodosdk.models import ClusterFilter
my_workspace = BodoWorkspaceClient()

clusters_conf = {
    'Team A': {
        'instance_type': 'c5.2xlarge',
        'workers': 4,
    },
    'Team b': {
        'instance_type': 'c5.xlarge',
        'workers': 2,
    },
    'Team C': {
        'instance_type': 'c5.16xlarge',
        'workers': 2,
    }
}
for owner, conf in clusters_conf.items():
    my_workspace.ClusterClient.create(
        name = f"{owner} Cluster",
        instance_type=conf['instance_type'],
        workers_quantity=conf['workers'],
        custom_tags={'owner': owner, 'purpose': 'test'}
    )

my_workspace.ClusterClient.list(
    filters=ClusterFilter(tags={'purpose': 'test'})
).wait_for_status(
    ['RUNNING', 'INITIALIZING']
).pause().wait_for_status(['PAUSED'])
```

## Use another cluster as a template for cluster definition in job

Let's imagine that you have a cluster (in any state) and you wan't to run job on the same specification, but you don't
want to use previously defined cluster. You can do following

```python
from bodosdk import BodoWorkspaceClient
my_workspace = BodoWorkspaceClient()
my_cluster = my_workspace.ClusterClient.get('existing_cluster')
cluster_conf = my_cluster.dict()
del cluster_conf['uuid']
my_sql_job = my_workspace.JobClient.run_sql_query(sql_query="SELECT 1", catalog="MyCatalog", cluster=cluster_conf)
```

In that case job will create a new cluster with provided configuration, executes and after job is finished
removes cluster.
