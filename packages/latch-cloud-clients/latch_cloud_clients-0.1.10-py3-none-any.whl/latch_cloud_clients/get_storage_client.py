from enum import Enum

from .aws.storage_client import S3StorageClient
from .gcp.storage_client import GCPStorageClient
from .utils import StorageClient


class LDataNodeType(str, Enum):
    account_root = "account_root"
    dir = "dir"
    obj = "obj"
    mount = "mount"
    link = "link"
    mount_gcp = "mount_gcp"
    mount_azure = "mount_azure"


def get_storage_client(root_type: LDataNodeType | None) -> StorageClient:
    if root_type is not None and root_type not in [
        LDataNodeType.account_root,
        LDataNodeType.mount,
        LDataNodeType.mount_gcp,
        LDataNodeType.mount_azure,
    ]:
        raise ValueError(f"Root is not a mount, got: {root_type}")

    if root_type == LDataNodeType.mount_gcp:
        return GCPStorageClient()
    else:
        return S3StorageClient()
