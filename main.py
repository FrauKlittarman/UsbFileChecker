import os
import subprocess
import hashlib
import shutil
import sys
from collections import namedtuple
from pathlib import Path
from packages.logger import logger

LPU_NAME = "Name"
URL = "https://localhost/post_item.php"

SOURCE_USB_NAME = "CLIPBOARD"
SOURCE_FILENAME = "clb.md"
TARGET_DIRECTORY = "/tmp/dest_dir"

MountPath = namedtuple("MountPath", ["prefix", "postfix"])


def get_os_name() -> str:
    # _os = (subprocess.check_output(["lsb_release", "-i"], text=True).split(":")[1].strip())
    # return _os
    return "MacOS"


def get_default_mount_path(_os_name: str = get_os_name()) -> MountPath:
    if _os_name == "RED SOFT":
        return MountPath(prefix="/run/media", postfix="")
    if _os_name == "MacOS":
        return MountPath(prefix="/Volumes", postfix="")
    else:
        return MountPath(prefix="/run/user", postfix="media")


def get_file_hash(file_path, algorithm="sha256"):
    path = Path(file_path)
    hash_func = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def _is_access_ok_to(_path: str, _check_parent: bool = False) -> bool:
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


def make_dest_dir(_target: str, _mode: oct = 0o750) -> None:
    if not _is_access_ok_to(_target) and _is_access_ok_to(_target, _check_parent=True):
        logger.debug(f"Make target directory: {_target}")
        try:
            Path(_target).mkdir(parents=True, mode=_mode)
        except FileExistsError as e:
            logger.error(f"Access problem: {_target}")
            sys.exit(1)
    elif not _is_access_ok_to(_target, _check_parent=True):
        logger.error(f"Access basedir problem: {_target}")


def upload_file(_path: str, _url: str = URL) -> None:
    try:
        t = subprocess.run(
            [
                "/usr/bin/curl",
                "-X",
                "POST",
                "-F",
                f"lpu={LPU_NAME}",
                "-F",
                f"file=@{_path}",
                _url,
            ],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        if t.returncode == 0:
            logger.info(f"Файл {_path} успешно загружен")

    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка загрузки файла:\n{e}")
        sys.exit(1)


def copy_src_to_dst(_src: str, _dst: str, _mode: oct = 0o650) -> None:
    shutil.copy2(_src, _dst)
    os.chmod(_dst, _mode)


def main() -> None:
    mount_path = get_default_mount_path()
    make_dest_dir(TARGET_DIRECTORY)
    dest_file_path = str(Path(TARGET_DIRECTORY).joinpath(SOURCE_FILENAME))

    if not _is_access_ok_to(dest_file_path):
        dest_file_hash_sum = ""
    else:
        dest_file_hash_sum = get_file_hash(dest_file_path)

    logger.debug(f"Dest file hash sum: {dest_file_hash_sum}")

    # Ищем директорию пользователя который примонтировал целевую флешку
    list_of_dirs = os.listdir(mount_path.prefix)
    for directory in list_of_dirs:
        # FIXME добавить имя УСБ для линуксов
        path_to_source_file = str(
            Path(mount_path.prefix).joinpath(
                directory, mount_path.postfix, SOURCE_FILENAME
            )
        )
        is_source_access_ok = _is_access_ok_to(path_to_source_file)
        logger.debug(f"Access to: {path_to_source_file} is {is_source_access_ok}")
        if is_source_access_ok and not dest_file_hash_sum:
            logger.debug("Dest file not found, copy from source")
            copy_src_to_dst(path_to_source_file, dest_file_path)
            upload_file(_path=dest_file_path)
        elif is_source_access_ok:
            source_file_hash = get_file_hash(path_to_source_file)
            logger.debug(f"Source file hash: {source_file_hash}")
            if source_file_hash != dest_file_hash_sum:
                logger.info("Файлы отличаются, выполняю замену.")
                copy_src_to_dst(path_to_source_file, dest_file_path)
                upload_file(_path=dest_file_path)
            else:
                logger.info("Файлы идентичны. прекращаю работу")


if __name__ == "__main__":
    logger.warning("=== Program start ===")
    try:
        main()
    except Exception as e:
        logger.error(f"Непредвиденная ошибка:\n{e}")
    logger.warning("=== Program end ===")
