from jtd_codebuild.config.project.model import CSharpTarget
from .._generator import JTDCodeGenerator


class CSharpJTDCodeGenerator(JTDCodeGenerator):
    def _codegen_command(self, target: CSharpTarget) -> str:
        schema_path = self.get_schema_path()
        output_dir = self.get_target_path(target)
        return (
            f"jtd-codegen {schema_path} "
            f"--csharp-system-text-out {output_dir} "
            f"--csharp-system-text-namespace {target.namespace}"
        )

    def generate(self, target: CSharpTarget) -> None:
        return super().generate(target)
