import os
import subprocess
from pathlib import Path
from typing import Union

import toml

from packages.exceptions import PyprojectFileNotFound


def _find_project_root(marker="pyproject.toml"):
    current = Path(__file__).parent
    while not (current / marker).exists():
        if current.parent == current:
            raise FileNotFoundError("Корень проекта не найден")
        current = current.parent
    return current


def _open_toml(
    _path: str, _section: str, _arg: str, _default: Union[str, bool, float] = None
) -> Union[str, bool]:
    """TODO: приделать нормальную валидацию и обработку ошибок"""
    try:
        with open(_path, "r") as f:
            data = toml.load(f)
        data = data[_section][_arg]
    except FileNotFoundError as e:
        raise PyprojectFileNotFound("pyproject.toml not found")
    except KeyError as e:
        data = _default
    return data


def get_os_name() -> str:
    _os = (
        subprocess.check_output(["lsb_release", "-i"], text=True).split(":")[1].strip()
    )
    return _os


PROJECT_ROOT = _find_project_root()
TOML_PATH = os.path.join(PROJECT_ROOT, "pyproject.toml")
PROJECT_NAME = _open_toml(TOML_PATH, "project", "name", "usbfilechecker")
AUTHOR = _open_toml(TOML_PATH, "project", "author", "KapVA")
RELEASE_YEAR = _open_toml(TOML_PATH, "project", "year", "2026")
PROJECT_VERSION = _open_toml(TOML_PATH, "project", "version", ">0.0.0")
SOURCE_FILENAME = _open_toml(TOML_PATH, "config", "filename", "datafile.xls")
SAVE_PATH = _open_toml(TOML_PATH, "config", "save_path", f"/usr/share/{PROJECT_NAME}")
TEMP_PATH = _open_toml(TOML_PATH, "config", "temp_path", f"/tmp/{PROJECT_NAME}")
LOG_PATH = _open_toml(TOML_PATH, "config", "log_path", "/var/log/")
