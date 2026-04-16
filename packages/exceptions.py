class PyprojectFileNotFound(Exception):
    """Затычка при открытии TOML"""

    pass


class FileAccessError(Exception):
    """Затычка при парсинге TOML"""

    pass
