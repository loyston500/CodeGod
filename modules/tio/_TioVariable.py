# coding=utf-8

from typing import AnyStr, List, Union


class TioVariable:
    _name = str()
    _content = []

    def __init__(self, name, content):
        # type: (AnyStr, Union[List[AnyStr], AnyStr]) -> None
        self._name = name
        self._content = content

    @property
    def name(self):
        # type: () -> AnyStr
        return self._name

    @property
    def content(self):
        # type: () -> List
        return self._content

    def get_name(self):
        # type: () -> AnyStr
        return self.name

    def get_content(self):
        # type: () -> List
        return self.content
