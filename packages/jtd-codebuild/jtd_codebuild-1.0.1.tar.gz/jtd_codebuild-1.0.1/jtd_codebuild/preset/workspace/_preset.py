from os import makedirs
from os.path import join, relpath, exists, dirname
from shutil import copyfile
from jtd_codebuild.values import WORKSPACE_CONFIG_NAME
from .._preset import Preset


class WorkspacePreset(Preset):
    def generate(self, cwd: str, **options):
        copy_config = [
            {
                "src": join(dirname(__file__), "templates", WORKSPACE_CONFIG_NAME),
                "dest": join(cwd, WORKSPACE_CONFIG_NAME),
            }
        ]
        for config in copy_config:
            if not exists(dirname(config["dest"])):
                makedirs(dirname(config["dest"]), exist_ok=True)
            copyfile(config["src"], config["dest"])
            self.logger.info(f"Created: {relpath(config['dest'], cwd)}")
