from . import _version
from .clients.workspace import BodoWorkspaceClient  # noqa
from .clients.organization import BodoOrganizationClient  # noqa

__version__ = _version.get_versions()["version"]
