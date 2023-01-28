import hashlib

from backup_mover_logger.logger import get_logger

logger = get_logger()


def calculate_sha256(path: str) -> str:
    logger.debug(f"Calculating sha256 for a file {path}")
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)

    sha = hash_sha256.hexdigest()
    logger.debug(f"Calculated sha {sha} for file {path}")
    return sha
