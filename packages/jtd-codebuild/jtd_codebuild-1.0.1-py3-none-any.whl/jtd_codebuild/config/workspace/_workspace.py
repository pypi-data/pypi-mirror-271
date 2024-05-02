from os.path import join, exists, dirname
from jtd_codebuild.values import WORKSPACE_CONFIG_NAME


def find_workspace_config_path(
    path: str,
    *,
    config_name: str = WORKSPACE_CONFIG_NAME,
) -> str | None:
    while True:
        config_path = join(path, config_name)
        if exists(config_path):
            return config_path

        parent = dirname(path)
        if parent == path:
            return None

        path = parent
