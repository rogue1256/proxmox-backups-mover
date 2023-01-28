import os


def get_related_files(source_path: os.path, vm_id: int) -> list[str]:
    files = os.listdir(source_path)
    related_files = []
    for name in files:
        if os.path.isfile(os.path.join(source_path, name)) and f"qemu-{vm_id}-" in name:
            related_files.append(name)

    return related_files
