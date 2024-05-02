from jtd_codebuild.config.project.model import JavaTarget
from .._generator import JTDCodeGenerator


class JavaJTDCodeGenerator(JTDCodeGenerator):
    def _codegen_command(self, target: JavaTarget) -> str:
        schema_path = self.get_schema_path()
        output_dir = self.get_target_path(target)
        return (
            f"jtd-codegen {schema_path} "
            f"--java-jackson-out {output_dir} "
            f"--java-jackson-package {target.package}"
        )

    def generate(self, target: JavaTarget) -> None:
        return super().generate(target)
