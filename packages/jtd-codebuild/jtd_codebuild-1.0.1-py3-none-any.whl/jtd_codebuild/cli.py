from typing import Callable
import click
from click.core import Context
from .commands import BuildCommand, InitCommand
from .logger import Logger, ClickLogger


@click.group(invoke_without_command=True)
@click.argument("path", type=click.Path(), required=False)
@click.option("--verbose", "-v", is_flag=True)
@click.pass_context
def cli(ctx: Context, path: str, verbose: bool):
    # If no subcommand is provided, run the build command
    if ctx.invoked_subcommand is None:
        logger = _create_logger(verbose)
        command = BuildCommand(logger=logger)
        _error_boundary(lambda: command.run(path or "."), logger)
    else:
        ctx.obj = {
            "path": path or ".",
            "verbose": verbose,
        }


@cli.command("init")
@click.pass_context
@click.option(
    "--preset",
    "-p",
    type=click.Choice(["config", "project", "workspace"]),
    default="config",
)
def init(ctx: Context, preset: str):
    path = ctx.obj["path"]
    verbose = ctx.obj["verbose"]

    logger = _create_logger(verbose)
    command = InitCommand(logger=logger)
    _error_boundary(lambda: command.run(path, preset), logger)


def _create_logger(verbose: bool) -> ClickLogger:
    return ClickLogger(level=1 if verbose else 2)


def _error_boundary(func: Callable, logger: Logger):
    try:
        func()
    except Exception as e:
        for line in str(e).split("\n"):
            logger.error(line)
        exit(1)
