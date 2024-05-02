import abc
import subprocess
from os import makedirs
from jtd_codebuild.component import Component
from jtd_codebuild.logger import Logger
from jtd_codebuild.config.project.model import Target
from jtd_codebuild.utils.fs import resolve
from jtd_codebuild.utils.subprocess import stream_logs


class JTDCodeGenerator(Component, metaclass=abc.ABCMeta):
    """Generate code from the JSON Type Definition files.

    Attributes:
        cwd: The current working directory.
        schema_path: The path to the JSON Type Definition schema file.
    """

    def __init__(
        self,
        cwd: str,
        schema_path: str,
        *,
        logger: Logger | None = None,
    ) -> None:
        self.cwd = cwd
        self.schema_path = schema_path
        super().__init__(logger=logger)

    def _codegen_command(
        self,
        target: Target,
    ) -> str:
        """Generate code from a JSON Type Definition schema file.

        Args:
            schema_path: The path to the JSON Type Definition schema file.
            output_dir: The output directory.
            target_language: The target language.

        Returns:
            The command to generate code.
        """
        schema_path = self.get_schema_path()
        output_dir = self.get_target_path(target)
        target_language = target.language
        return f"jtd-codegen {schema_path} --{target_language}-out {output_dir}"

    def generate(self, target: Target) -> None:
        """Generate code from the JSON Type Definition files.

        Args:
            target: Target configuration.

        Returns:
            A list of subprocesses created by the code generation.
        """
        makedirs(self.get_target_path(target), exist_ok=True)
        process = subprocess.Popen(
            self._codegen_command(target),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stream_logs(process, logger=self.logger, level="debug")
        process.wait()

    def get_schema_path(self) -> str:
        return resolve(self.cwd, self.schema_path)

    def get_target_path(self, target: Target) -> str:
        return resolve(self.cwd, target.path)
