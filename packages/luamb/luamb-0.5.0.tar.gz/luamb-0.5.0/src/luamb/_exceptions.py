from __future__ import annotations


class LuambException(Exception):
    message: str | None = None

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message

    def __str__(self) -> str:
        return self.message or self.__class__.__name__


class ImproperlyConfigured(LuambException):
    pass
