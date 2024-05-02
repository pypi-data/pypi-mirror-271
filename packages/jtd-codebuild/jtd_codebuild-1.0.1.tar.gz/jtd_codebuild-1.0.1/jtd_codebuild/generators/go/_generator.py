from jtd_codebuild.config.project.model import GoTarget
from .._generator import JTDCodeGenerator


class GoJTDCodeGenerator(JTDCodeGenerator):
    def _codegen_command(self, target: GoTarget) -> str:
        schema_path = self.get_schema_path()
        output_dir = self.get_target_path(target)
        return (
            f"jtd-codegen {schema_path} "
            f"--go-out {output_dir} "
            f"--go-package {target.package}"
        )

    def generate(self, target: GoTarget) -> None:
        return super().generate(target)
