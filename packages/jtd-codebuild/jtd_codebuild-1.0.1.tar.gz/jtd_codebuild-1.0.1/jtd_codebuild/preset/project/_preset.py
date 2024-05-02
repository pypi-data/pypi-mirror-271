from os import makedirs
from os.path import join, relpath, dirname, exists
from shutil import copyfile
from jtd_codebuild.values import CONFIG_NAME
from .._preset import Preset


class ProjectPreset(Preset):
    def generate(self, cwd: str, **options):
        copy_config = [
            {
                "src": join(dirname(__file__), "templates", CONFIG_NAME),
                "dest": join(cwd, CONFIG_NAME),
            },
            {
                "src": join(dirname(__file__), "templates", ".gitignore"),
                "dest": join(cwd, ".gitignore"),
            },
        ]
        for config in copy_config:
            if not exists(dirname(config["dest"])):
                makedirs(dirname(config["dest"]), exist_ok=True)
            copyfile(config["src"], config["dest"])
            self.logger.info(f"Created: {relpath(config['dest'], cwd)}")

        mkdir_config = [
            join(cwd, "src"),
            join(cwd, "gen"),
        ]
        for directory in mkdir_config:
            makedirs(directory, exist_ok=True)
            self.logger.info(f"Created: {relpath(directory, cwd)}")
