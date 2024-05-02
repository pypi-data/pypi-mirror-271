import json
from os.path import join, dirname
from toolz import pipe
from jtd_codebuild.utils.io import read_json
from jtd_codebuild.utils.function import replace
from jtd_codebuild.values import CONFIG_NAME
from ..workspace import find_workspace_config_path
from .model import ProjectConfig


def get_project_config(
    cwd: str,
    *,
    project_root: str = "<projectRoot>",
    workspace_root: str = "<workspaceRoot>",
) -> ProjectConfig:
    """Get configutation from :const:`CONFIG_NAME`_ file
    in the current working directory.

    Args:
        cwd: The current working directory.

    Returns:
        The configuration dictionary.
    """
    config = pipe(
        read_json(join(cwd, CONFIG_NAME)),
        json.dumps,
        replace(project_root, cwd),
        replace(
            workspace_root,
            pipe(
                find_workspace_config_path(cwd),
                lambda path: path and dirname(path) or cwd,
            ),
        ),
        json.loads,
    )
    return ProjectConfig(**config)
