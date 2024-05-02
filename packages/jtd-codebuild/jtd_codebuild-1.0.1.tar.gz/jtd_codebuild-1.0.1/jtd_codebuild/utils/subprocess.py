import subprocess
from jtd_codebuild.logger import Logger


def flush_streams_to_logs(
    process: subprocess.Popen,
    *,
    logger: Logger,
    level: str = "info",
):
    pipe_data = process.communicate()
    for data in pipe_data:
        if data:
            for line in data.decode().split("\n"):
                logger[level](line)


def stream_logs(
    process: subprocess.Popen,
    *,
    logger: Logger,
    level: str = "info",
):
    while process.returncode is None:
        flush_streams_to_logs(process, logger=logger, level=level)
    flush_streams_to_logs(process, logger=logger, level=level)
