# coding=utf-8

from typing import AnyStr


class TioFile:
    _name = str()
    _content = bytes()

    def __init__(self, name, content):
        # type: (AnyStr, bytes) -> None
        self._name = name
        self._content = content

    def get_name(self):
        # type: () -> AnyStr
        return self.name

    def get_content(self):
        # type: () -> bytes
        return self.content

    @property
    def name(self):
        # type: () -> AnyStr
        return self._name

    @property
    def content(self):
        # type: () -> bytes
        return self._content
