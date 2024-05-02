from caseconverter import pascalcase, camelcase, snakecase
from jtd_codebuild.config.project.model import PropertyFormat


def caseconverter(
    case: PropertyFormat,
    target: str,
) -> str:
    if case == "snake":
        return snakecase(target)
    if case == "camel":
        return camelcase(target)
    if case == "pascal":
        return pascalcase(target)
    raise ValueError(f"Unknown case: {case}")
