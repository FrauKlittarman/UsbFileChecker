import hashlib
import os
import shutil
import sys
from pathlib import Path

from packages.logger import logger


def is_access_ok_to(_path: str, _check_parent: bool = False) -> bool:
    if _check_parent:
        if os.access(Path(_path).parent, os.R_OK) and os.access(
            Path(_path).parent, os.W_OK
        ):
            return True
        else:
            return False
    if os.access(_path, os.R_OK) and os.access(_path, os.W_OK):
        return True
    return False


def make_dest_dir(_target: str, _mode: int = 0o750) -> None:
    if not is_access_ok_to(_target) and is_access_ok_to(_target, _check_parent=True):
        logger.debug(f"Make target directory: {_target}")
        try:
            Path(_target).mkdir(parents=True, mode=_mode)
        except FileExistsError:
            logger.error("Ошибка доступа к целевой директории")
            sys.exit(1)
    elif not is_access_ok_to(_target, _check_parent=True):
        logger.error(f"Access basedir problem: {_target}")


def copy_src_to_dst(_src: str, _dst: str, _mode: int = 0o640) -> None:
    shutil.copy2(_src, _dst)
    os.chmod(_dst, _mode)


def get_file_hash(file_path: str, algorithm="sha256") -> str:
    path = Path(file_path)
    hash_func = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()
