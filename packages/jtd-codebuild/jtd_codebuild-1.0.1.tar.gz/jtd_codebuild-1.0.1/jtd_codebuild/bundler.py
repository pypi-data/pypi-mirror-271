import yaml
import json
import os
import itertools
from os.path import join
from typing import Generator, Tuple
from copy import deepcopy
from toolz import pipe
from toolz.curried import map, get, curry
from .config.project import get_project_config
from .config.project.model import ProjectConfig
from .utils import fs
from .component import Component

ROOT_SCHEMA = {
    "metadata": {"description": ""},
    "definitions": {},
}
"""As jtd-codegen requires for root schema to be defined, 
this tool defines it as an empty object.

This root schema will be removed after the code generation process.
"""


class Bundler(Component):
    """Bundle JSON Type Definition files."""

    def bundle(
        self,
        cwd: str,
        config: ProjectConfig | None = None,
    ) -> dict:
        config = config or get_project_config(cwd)

        resolve = curry(fs.resolve)(cwd)

        # Bundle reference schemas
        schemas: list[dict] = pipe(
            config.references,
            map(resolve),
            map(self.bundle),
        )

        # Extract definitions from includes schemas
        # and this config's ones
        definitions: list[dict] = pipe(
            schemas,
            map(get("definitions", default={})),
            list,
        ) + [self.bundle_definitions(cwd, config)]

        # Bundle all definitions
        bundled_schema = deepcopy(ROOT_SCHEMA)
        for name, definition in pipe(
            definitions,
            map(items),
            itertools.chain.from_iterable,
        ):
            if name in bundled_schema["definitions"] and config.duplicate == "error":
                raise ValueError(f"Duplicate definition: {name}")
            bundled_schema["definitions"][name] = definition

        return bundled_schema

    def bundle_definitions(
        self,
        cwd: str,
        config: ProjectConfig,
    ) -> dict:
        resolve = curry(fs.resolve)(cwd)

        def file_is_idl(file: str) -> bool:
            return fs.file_is_json(file) or fs.file_is_yaml(file)

        def load_idl(file: str) -> dict:
            with open(file, "r") as f:
                if fs.file_is_yaml(file):
                    return yaml.load(f, Loader=yaml.SafeLoader)
                else:
                    return json.load(f)

        # Recursively load all definitions
        def load_all_definitions(
            roots: list[str],
        ) -> Generator[Tuple[str, dict], None, None]:
            lookup = set()
            for root, dirs, files in pipe(
                roots,
                map(os.walk),
                itertools.chain.from_iterable,
            ):
                for file in files:
                    if file_is_idl(file):
                        filepath = join(root, file)
                        definitions = load_idl(filepath)
                        for name, definition in definitions.items():
                            if name in lookup:
                                raise ValueError(
                                    f"Definition name {name} already exists."
                                )
                            yield name, definition
                            lookup.add(name)

        definition_roots = pipe(config.include, map(resolve), list)

        return dict(load_all_definitions(definition_roots))


def items(d: dict):
    return d.items()
