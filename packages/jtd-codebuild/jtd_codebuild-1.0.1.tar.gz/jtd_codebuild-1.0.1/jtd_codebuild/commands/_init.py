from os import getcwd
from jtd_codebuild.utils.fs import resolve
from jtd_codebuild.preset.config import ConfigPreset
from jtd_codebuild.preset.workspace import WorkspacePreset
from jtd_codebuild.preset.project import ProjectPreset
from ._command import Command


class InitCommand(Command):
    def run(
        self,
        path: str,
        preset: str,
        cwd: str = getcwd(),
    ):
        self.logger.info(f"Initializing project at {path} with preset {preset}")

        path = resolve(cwd, path)

        if preset == "config":
            ConfigPreset(logger=self.logger).generate(path)
        elif preset == "workspace":
            WorkspacePreset(logger=self.logger).generate(path)
        elif preset == "project":
            ProjectPreset(logger=self.logger).generate(path)
        else:
            raise ValueError(f"Unknown preset {preset}")
