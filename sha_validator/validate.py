import hashlib
import os


def calculate_sha256(path: str) -> str:
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def validate_files(file1: os.path, file2: os.path) -> bool:
    return calculate_sha256(file1) == calculate_sha256(file2)
