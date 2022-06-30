import typing as t
import path
import sys


class Config(object):
    _paths: t.Dict[str, str]

    def __init__(self):
        self._paths = dict()

    # def serialize(self) -> t.Any:
    #     return pickle.dumps(self)

    # @classmethod
    # def deserialize(cls, content: t.Any):
    #     return pickle.loads(content)

    # @classmethod
    # def from_file(cls, content: t.Any):
    #     return pickle.loads(content)

    def get_path(self, key: str) -> path.Path:
        if key not in self._paths:
            raise KeyError("Path not defined")
        return path.Path(self._paths[key])

    def set_path(self, key, path: str):
        self._paths[key] = path

    def remove_path(self, key) -> None:
        self._paths.pop(key, None)
