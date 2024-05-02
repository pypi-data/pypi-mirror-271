from ._logger import Logger


class NoopLogger(Logger):
    def debug(self, message: str, *args, **kwargs) -> None:
        pass

    def info(self, message: str, *args, **kwargs) -> None:
        pass

    def success(self, message: str, *args, **kwargs) -> None:
        pass

    def warning(self, message: str, *args, **kwargs) -> None:
        pass

    def error(self, message: str, *args, **kwargs) -> None:
        pass
