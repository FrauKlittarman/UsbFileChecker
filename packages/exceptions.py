class PyprojectFileNotFound(Exception):
    """Затычка при открытии TOML"""

    pass


class TomlValidateError(Exception):
    """Затычка при парсинге TOML"""

    pass


class AppNotFoundError(Exception):
    """Feh not found"""

    pass


class JSONFileIsEmpty(Exception):
    """JSON is empty"""

    pass
