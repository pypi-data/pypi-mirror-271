from os.path import join
from typing import Generator, Tuple
from toolz import pipe, compose_left
from toolz.curried import curry
from jtd_codebuild.config.project.model import TypescriptTarget, PropertyFormat
from jtd_codebuild.utils.io import read_json, write_json, read, write
from jtd_codebuild.utils.function import replace
from jtd_codebuild.utils.string import caseconverter
from .._generator import JTDCodeGenerator


class TypescriptJTDCodeGenerator(JTDCodeGenerator):
    """Generate Typescript code from the JSON Type Definition files."""

    def generate(self, target: TypescriptTarget) -> None:
        jtd_schema_path = self.get_schema_path()

        jtd_schema = read_json(jtd_schema_path)
        definitions: dict = jtd_schema.get("definitions", {})

        propertyFormat = target.propertyFormat

        if propertyFormat:
            convert_property_keys = compose_left(
                curry(convert_keys_case)(propertyFormat),
                dict,
            )

            def convert_definition_keys_case(definition: dict) -> None:
                if "discriminator" in definition:
                    definition["discriminator"] = caseconverter(
                        propertyFormat,
                        definition["discriminator"],
                    )
                    for case_ in definition["mapping"].values():
                        convert_definition_keys_case(case_)
                else:
                    properties = definition.get("properties", None)
                    if properties:
                        definition["properties"] = convert_property_keys(properties)
                    optionalProperties = definition.get("optionalProperties", None)
                    if optionalProperties:
                        definition["optionalProperties"] = convert_property_keys(
                            optionalProperties
                        )

            for class_name in definitions.keys():
                definition = definitions[class_name]
                convert_definition_keys_case(definition)

        write_json(jtd_schema_path, jtd_schema)

        # Generate the target
        super().generate(target)

        target_path = join(self.get_target_path(target), "index.ts")
        schema = read(target_path)

        if target.removeRootSchema:
            schema = pipe(
                schema,
                replace("export type Schema = any;", ""),
                replace("export type JtdSchema = any;", ""),
            )

        write(
            target_path,
            ("/* eslint-disable */\n" + "/* tslint:disable */\n" + schema),
        )


def convert_keys_case(
    propertyFormat: PropertyFormat,
    properties: dict,
) -> Generator[Tuple[str, dict], None, None]:
    for property_name, property_definition in properties.items():
        yield (
            caseconverter(
                propertyFormat,
                property_name,
            ),
            property_definition,
        )
