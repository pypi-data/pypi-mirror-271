from os import getcwd
from os.path import relpath
from typing import Callable, Type
from toolz import pipe
from toolz.curried import map
from .utils.fs import resolve
from .utils.io import write_json
from .bundler import Bundler
from .inheritance import InheritanceResolver
from .component import Component
from .config.project import get_project_config
from .config.project.model import Language, Target
from .generators import JTDCodeGenerator
from .generators.python import PythonJTDCodeGenerator
from .generators.typescript import TypescriptJTDCodeGenerator
from .generators.go import GoJTDCodeGenerator
from .generators.java import JavaJTDCodeGenerator
from .generators.ruby import RubyJTDCodeGenerator
from .generators.rust import RustJTDCodeGenerator
from .generators.csharp import CSharpJTDCodeGenerator

GENERATORS: dict[Language, Type[JTDCodeGenerator]] = {
    "python": PythonJTDCodeGenerator,
    "typescript": TypescriptJTDCodeGenerator,
    "go": GoJTDCodeGenerator,
    "java": JavaJTDCodeGenerator,
    "ruby": RubyJTDCodeGenerator,
    "rust": RustJTDCodeGenerator,
    "csharp": CSharpJTDCodeGenerator,
}


class Codebuild(Component):
    def run(  # noqa: C901
        self,
        path: str,
        cwd: str = getcwd(),
    ):
        """Generate code from the JSON Type Definition files.

        Args:
            path: The current working directory.
        """
        # Get the path of the target directory
        target_path = resolve(cwd, path)
        config = get_project_config(target_path)

        self.logger.info(f"Start building: {path}")

        self.logger.info("Bundling IDL files...")
        bundler = Bundler(logger=self.logger)
        inheritance = InheritanceResolver(logger=self.logger)
        bundled_jtd_schema = pipe(
            bundler.bundle(target_path, config),
            inheritance.resolve,
        )

        schema_path = resolve(target_path, config.jtdBundlePath)
        write_json(schema_path, bundled_jtd_schema)

        self.logger.success(f"Wrote bundled IDL file at: {relpath(schema_path, cwd)}")

        self.logger.info("Generating targets...")

        context = {
            "cwd": target_path,
            "schema_path": schema_path,
            "logger": self.logger,
        }

        def create_generator(target: Target) -> Callable[[], None]:
            def generate() -> None:
                generator = GENERATORS[target.language](**context)
                generator.generate(target)

            return generate

        generators = pipe(config.targets, map(create_generator))
        if config.targetProcessingStrategy == "serial":
            for generator in generators:
                generator()
        else:
            from joblib import Parallel, delayed

            Parallel(n_jobs=-1)(delayed(generator)() for generator in generators)

        self.logger.success("Done!")
