import abc
from typing import Literal, TypeAlias
from jtd_codebuild.utils.mapping import Subscriptable

Level: TypeAlias = Literal[
    1,  # DEBUG
    2,  # INFO
    3,  # SUCCESS
    4,  # WARNING
    5,  # ERROR
]


class Logger(Subscriptable, metaclass=abc.ABCMeta):
    def __init__(self, level: Level = 2) -> None:
        self.level = level

    @abc.abstractmethod
    def debug(self, message: str, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def info(self, message: str, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def success(self, message: str, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def warning(self, message: str, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def error(self, message: str, *args, **kwargs) -> None:
        pass
