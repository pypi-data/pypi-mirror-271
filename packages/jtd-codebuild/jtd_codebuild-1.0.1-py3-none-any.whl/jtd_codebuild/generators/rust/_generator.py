from jtd_codebuild.config.project.model import RustTarget
from .._generator import JTDCodeGenerator


class RustJTDCodeGenerator(JTDCodeGenerator):
    def generate(self, target: RustTarget) -> None:
        return super().generate(target)
