from pydantic import BaseModel, Field
from ._types import DuplicatePolicy, TargetProcessingStrategy
from ._target import (
    PythonTarget,
    TypescriptTarget,
    GoTarget,
    JavaTarget,
    CSharpTarget,
    RustTarget,
    RubyTarget,
)
from jtd_codebuild.utils.mapping import Subscriptable


class ProjectConfig(BaseModel, Subscriptable):
    include: list[str] = Field(default_factory=lambda: [])
    references: list[str] = Field(default_factory=lambda: [])
    targets: list[
        PythonTarget
        | TypescriptTarget
        | GoTarget
        | JavaTarget
        | CSharpTarget
        | RustTarget
        | RubyTarget
    ] = Field(default_factory=lambda: [])
    targetProcessingStrategy: TargetProcessingStrategy = "parallel"
    jtdBundlePath: str = "gen/schema.jtd.json"
    duplicate: DuplicatePolicy = "error"
