from dataclasses import dataclass
from enum import Enum

from config_provider.models import VmInfo


class FailReason(Enum):
    Unknown = 0
    DifferentSha256 = 1
    CopyFailed = 2


@dataclass
class VmFilesCopyResult:
    vm: VmInfo
    copied_files: [(str, str)]
    failed_copies: [(str, FailReason)]
