import os
from dataclasses import dataclass


@dataclass
class BackupInfo:
    friendly_name: str
    vm_id: int
    target_path: os.path


@dataclass
class BackupConfig:
    """Config information"""
    source_path: str
    vm_configs: list[BackupInfo]
    log_level: str
