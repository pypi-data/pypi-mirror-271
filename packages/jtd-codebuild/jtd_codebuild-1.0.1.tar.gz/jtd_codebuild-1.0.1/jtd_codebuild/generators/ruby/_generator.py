from jtd_codebuild.config.project.model import RubyTarget
from .._generator import JTDCodeGenerator


class RubyJTDCodeGenerator(JTDCodeGenerator):
    def _codegen_command(self, target: RubyTarget) -> str:
        schema_path = self.get_schema_path()
        output_dir = self.get_target_path(target)
        return (
            f"jtd-codegen {schema_path} "
            f"--ruby-out {output_dir} "
            f"--ruby-module {target.module}"
        )

    def generate(self, target: RubyTarget) -> None:
        return super().generate(target)
