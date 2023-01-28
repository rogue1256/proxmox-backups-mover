import os
from dataclasses import dataclass


@dataclass
class VmInfo:
    friendly_name: str
    vm_id: int
    target_path: os.path


@dataclass
class BackupMoverConfig:
    """Config information"""
    source_path: str
    vm_configs: list[VmInfo]
    log_level: str
    telegram_AT: str
    chat_id: int
