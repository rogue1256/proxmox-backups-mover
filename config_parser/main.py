import os
import json
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


def parse_config(absolute_path: str) -> BackupConfig:
    with open(absolute_path, 'r') as config_file:
        config: dict = json.load(config_file)
        source_path = os.path.join(*config.get("backup_source_path"))
        target_path = os.path.join(*config.get("backup_target_path"))
        vm_list: list[BackupInfo] = []
        for vm in config.get("backup_configs"):
            friendly_name = vm.get("friendly_name")
            vm_id = vm.get("vm_id")
            vm_target_path = os.path.join(target_path, *vm.get("target_path_in_cloud"))
            vm_list.append(BackupInfo(friendly_name, vm_id, vm_target_path))
        return BackupConfig(source_path, vm_list)