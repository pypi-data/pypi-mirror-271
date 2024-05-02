from ._command import Command
from jtd_codebuild.codebuild import Codebuild


class BuildCommand(Command):
    def run(self, path: str):
        return Codebuild(logger=self.logger).run(path)
