import inspect
import ast
from ast import (
    ClassDef,
    Name,
    Load,
    AnnAssign,
    Constant,
    Import,
    ImportFrom,
    FunctionDef,
    Expr,
    Call,
)
from os.path import dirname, join
from io import TextIOWrapper
from typing import Type, Any, Tuple, TypeVar
from caseconverter import pascalcase
from toolz import pipe
from toolz.curried import filter, map, complement, valfilter
from jtd_codebuild.config.project.model import PythonTarget
from jtd_codebuild.utils.io import read, read_json
from jtd_codebuild.utils.string import caseconverter
from jtd_codebuild.utils.list import find, find_one
from jtd_codebuild.utils.function import replace
from .._values import ROOT_SCHEMA_NAMES
from .._generator import JTDCodeGenerator

SUBSCRIPTABLE_SOURCE_CODE = read(
    join(
        dirname(__file__),
        "../..",
        "utils/mapping/_subscriptable.py",
    )
)


class PythonJTDCodeGenerator(JTDCodeGenerator):
    """Generate Python code from the JSON Type Definition files."""

    def generate(self, target: PythonTarget) -> None:  # noqa: C901
        # Generate the target
        super().generate(target)

        # Open the schema file
        with self._open_schema_file(target, "r") as f:
            code = f.read()

        # Parse the schema file
        parsed = ast.parse(code)

        imports: list[Import] = select_nodes_by_type(Import, parsed.body)
        importfroms: list[ImportFrom] = select_nodes_by_type(ImportFrom, parsed.body)
        classes: list[ClassDef] = select_nodes_by_type(ClassDef, parsed.body)
        schemas: list[ClassDef] = pipe(classes, filter(complement(is_enum_class)), list)
        enums: list[ClassDef] = pipe(classes, filter(is_enum_class), list)
        functions: list[FunctionDef] = select_nodes_by_type(FunctionDef, parsed.body)
        calls: list[Call] = []

        # Open the jtd schema file
        jtd_schema = read_json(self.get_schema_path())

        # Find discriminators
        discriminators: dict[str, dict] = pipe(
            jtd_schema["definitions"],
            valfilter(lambda value: "discriminator" in value),
        )

        def get_discriminator_cases_of(discriminator: str) -> list[str]:
            return pipe(
                discriminators[discriminator]["mapping"].keys(),
                list,
            )

        def get_discriminator_name_of(discriminator: str) -> str:
            return discriminators[discriminator]["discriminator"]

        def is_discriminator_base(class_or_class_name: ClassDef | str) -> bool:
            if not isinstance(class_or_class_name, (ClassDef, str)):
                return False
            class_name = (
                class_or_class_name.name
                if isinstance(class_or_class_name, ClassDef)
                else class_or_class_name
            )
            return class_name in discriminators.keys()

        def is_discriminator_case(class_: ClassDef) -> bool:
            return isinstance(class_, ClassDef) and any(
                base.id in discriminators.keys() for base in class_.bases
            )

        # Add discriminator metadata to base discriminator schemas
        for discriminator in pipe(schemas, filter(is_discriminator_base)):
            base = discriminator.name
            discriminator.__dict__["__discriminator_meta__"] = {
                "type": "base",
                "discriminator": get_discriminator_name_of(base),
                "cases": pipe(
                    get_discriminator_cases_of(base),
                    map(lambda case_: (case_, base + pascalcase(case_))),
                    dict,
                ),
            }

        # Add discriminator metadata to discriminator case schemas
        for discriminator in pipe(schemas, filter(is_discriminator_case)):
            base = find_one(
                lambda base: is_discriminator_base(base.id),
                discriminator.bases,
            )
            discriminator.__dict__["__discriminator_meta__"] = {
                "type": "case",
                "discriminator": get_discriminator_name_of(base.id),
                "base": base.id,
                "case": find_one(
                    lambda case_: pascalcase(case_)
                    == discriminator.name.replace(base.id, ""),
                    get_discriminator_cases_of(base.id),
                ),
            }

        # Remove root schema from the file if the option is set
        if target.removeRootSchema:
            schemas = find(
                lambda node: node.name not in ROOT_SCHEMA_NAMES,
                schemas,
            )

        def add_import_from(module: str, names: list[str] = []) -> ImportFrom:
            importfrom = create_importfrom_directive(module, names)
            importfroms.append(importfrom)
            return importfrom

        def create_discriminator_base_json_codec_method(
            schema: ClassDef,
        ) -> list[FunctionDef]:
            metadata = schema.__dict__["__discriminator_meta__"]
            from_json_data = create_discriminator_base_from_json_data_method(
                schema.name,
                metadata["discriminator"],
                metadata["cases"],
            )
            to_json_data = create_discriminator_base_to_json_data_method()
            return [from_json_data, to_json_data]

        def create_discriminator_case_json_codec_method(
            schema: ClassDef,
        ) -> list[FunctionDef]:
            properties = select_nodes_by_type(AnnAssign, schema.body)
            metadata = schema.__dict__["__discriminator_meta__"]
            from_json_data = create_from_json_data_method(
                [f'"{metadata["case"]}"'] + properties,
                return_type=schema.name,
            )
            to_json_data = create_to_json_data_method(
                properties,
                initial_value={metadata["discriminator"]: metadata["case"]},
            )
            return [from_json_data, to_json_data]

        def create_json_codec_method(schema: ClassDef) -> list[FunctionDef]:
            if is_discriminator_base(schema):
                return create_discriminator_base_json_codec_method(schema)
            elif is_discriminator_case(schema):
                return create_discriminator_case_json_codec_method(schema)
            else:
                properties = select_nodes_by_type(AnnAssign, schema.body)
                from_json_data = create_from_json_data_method(
                    properties,
                    return_type=schema.name,
                )
                to_json_data = create_to_json_data_method(properties)
            return [from_json_data, to_json_data]

        def create_pydantic_json_codec_method(schema: ClassDef) -> list[FunctionDef]:
            if is_discriminator_base(schema):
                return create_discriminator_base_json_codec_method(schema)
            else:
                from_json_data = create_pydantic_from_json_data_method(schema.name)
                to_json_data = create_pydantic_to_json_data_method()
            return [from_json_data, to_json_data]

        def create_pydantic_dataclass_json_codec_method(
            schema: ClassDef,
        ) -> list[FunctionDef]:
            if is_discriminator_base(schema):
                return create_discriminator_base_json_codec_method(schema)
            else:
                from_json_data = create_pydantic_from_json_data_method(schema.name)
                to_json_data = create_pydantic_dataclass_to_json_data_method()
            return [from_json_data, to_json_data]

        def postprocess_for_dataclass():
            for schema in schemas:
                schema.body = remove_json_codec_methods(schema.body)
                schema.body.extend(create_json_codec_method(schema))

                if target.subscriptable:
                    inherit("Subscriptable", schema)

                for property in select_nodes_by_type(AnnAssign, schema.body):
                    # Change type annotations to actual implementations
                    annotation: str = property.annotation.value
                    property.annotation.value = use_implementation_type(annotation)

                    # Add `None` to optional fields
                    if annotation.startswith("Optional"):
                        property.value = Constant(value=None)

                    # Convert property names to given format if given
                    if target.propertyFormat:
                        format_property_name(target.propertyFormat, property)

        def postprocess_for_pydantic():
            nonlocal importfroms, functions
            importfroms = remove_dataclass_imports(importfroms)
            functions = remove_json_codec_helpers(functions)

            add_import_from("pydantic", ["BaseModel"])

            for enum in enums:
                enum.body = remove_json_codec_methods(enum.body)

            for schema in schemas:
                schema.body = remove_json_codec_methods(schema.body)
                schema.body.extend(create_pydantic_json_codec_method(schema))

                inherit("BaseModel", schema)
                if target.subscriptable:
                    inherit("Subscriptable", schema)

                schema.decorator_list = remove_dataclass_decorator(
                    schema.decorator_list
                )

                for property in select_nodes_by_type(AnnAssign, schema.body):
                    # Change type annotations to actual implementations
                    annotation: str = property.annotation.value
                    property.annotation.value = use_implementation_type(annotation)

                    # Add `None` to optional fields
                    if annotation.startswith("Optional"):
                        property.value = Constant(value=None)

                    # Convert property names to given format if given
                    if target.propertyFormat:
                        format_property_name(target.propertyFormat, property)

        def postprocess_for_pydantic_dataclass():
            nonlocal importfroms, functions
            importfroms = remove_dataclass_imports(importfroms)
            functions = remove_json_codec_helpers(functions)

            add_import_from("pydantic.dataclasses", ["dataclass", "rebuild_dataclass"])

            for schema in schemas:
                schema.body = remove_json_codec_methods(schema.body)
                schema.body.extend(create_pydantic_dataclass_json_codec_method(schema))

                if target.subscriptable:
                    inherit("Subscriptable", schema)

                for property in select_nodes_by_type(AnnAssign, schema.body):
                    # Change type annotations to actual implementations
                    annotation: str = property.annotation.value
                    property.annotation.value = use_implementation_type(annotation)

                    # Add `None` to optional fields
                    if annotation.startswith("Optional"):
                        property.value = Constant(value=None)

                    # Convert property names to given format if given
                    if target.propertyFormat:
                        format_property_name(target.propertyFormat, property)

                calls.append(create_call_directive("rebuild_dataclass", [schema.name]))

        def postprocess_for_typed_dictionary():
            nonlocal importfroms, functions
            importfroms = remove_dataclass_imports(importfroms)
            functions = remove_json_codec_helpers(functions)

            add_import_from("typing", ["TypedDict"])

            for schema in schemas:
                schema.body = remove_json_codec_methods(schema.body)

                inherit("TypedDict", schema)
                if target.subscriptable:
                    inherit("Subscriptable", schema)

                schema.decorator_list = remove_dataclass_decorator(
                    schema.decorator_list
                )

                for property in select_nodes_by_type(AnnAssign, schema.body):
                    # Change type annotations to actual implementations
                    annotation: str = property.annotation.value
                    property.annotation.value = use_implementation_type(annotation)

                    # Convert property names to given format if given
                    if target.propertyFormat:
                        format_property_name(target.propertyFormat, property)

        if target.typingBackend == "dataclass":
            postprocess_for_dataclass()
        elif target.typingBackend == "pydantic":
            postprocess_for_pydantic()
        elif target.typingBackend == "pydantic-dataclass":
            postprocess_for_pydantic_dataclass()
        elif target.typingBackend == "typed-dictionary":
            postprocess_for_typed_dictionary()
        else:
            raise ValueError(f"Unsupported typing backend: {target.typingBackend}")

        # Add subscriptable code if the option is set
        if target.subscriptable:
            subscriptable = ast.parse(SUBSCRIPTABLE_SOURCE_CODE)
            schemas = subscriptable.body + schemas

        # Merge every nodes
        nodes = imports + importfroms + schemas + enums + functions + calls

        # Write back the code
        code = (
            "# Code generated by jtd-codebuild\n"
            + "# flake8: noqa\n"
            + "# pylint: skip-file\n"
            + "# fmt: off\n"
            + ast.unparse(nodes)
        )
        with self._open_schema_file(target, "w") as f:
            f.write(code)

    def _open_schema_file(self, target: PythonTarget, mode: str) -> TextIOWrapper:
        output_dir = join(self.get_target_path(target), "__init__.py")
        return open(output_dir, mode)


def create_call_directive(
    func: str,
    args: list[str] = [],
    kwargs: dict[str, str] = {},
) -> Expr:
    return ast.parse(
        func
        + "("
        + ", ".join(args)
        + ", "
        + ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        + ")"
    ).body[0]


def create_importfrom_directive(
    module: str,
    names: list[str] = [],
) -> ImportFrom:
    return ast.parse(f'from {module} import {", ".join(names)}').body[0]


def create_from_json_data_method(
    properties: list[AnnAssign | str],
    return_type: ClassDef | str,
) -> FunctionDef:
    # Convert return type to string if it is a ClassDef
    if isinstance(return_type, ClassDef):
        return_type = return_type.name

    def create_argument_directive(
        property: AnnAssign | str,
    ) -> str:
        if isinstance(property, AnnAssign):
            # If the property is an AnnAssign node, create a directive
            # that converts the property from JSON data to python data
            return (
                f"_from_json_data({property.annotation.value}, "
                f"data.get('{property.target.id}'))"
            )
        else:
            # If string literal is given, return it as is
            return property

    arguments = ", ".join(pipe(properties, map(create_argument_directive)))
    source = inspect.cleandoc(
        f"""
    @classmethod
    def from_json_data(cls, data: Any) -> '{return_type}':
        return cls({arguments})
    """
    )
    return ast.parse(source).body[0]


def create_discriminator_base_from_json_data_method(
    base: str,
    discriminator: str,
    cases: dict[str, str],
) -> FunctionDef:
    def create_discriminator_entry(item: Tuple[str, str]) -> str:
        case_, class_ = item
        return f'"{case_}": {class_}'

    entries = ", ".join(pipe(cases.items(), map(create_discriminator_entry)))
    source = inspect.cleandoc(
        f"""
    @classmethod
    def from_json_data(cls, data: Any) -> '{base}':
        return {{{entries}}}[data['{discriminator}']].from_json_data(data)
    """
    )
    return ast.parse(source).body[0]


def create_pydantic_from_json_data_method(
    name: str,
) -> FunctionDef:
    source = inspect.cleandoc(
        f"""
    @classmethod
    def from_json_data(cls, data: Any) -> '{name}':
        return cls(**data)
    """
    )
    return ast.parse(source).body[0]


def create_pydantic_to_json_data_method() -> FunctionDef:
    source = inspect.cleandoc(
        """
    def to_json_data(self, **kwargs) -> Any:
        return self.model_dump(**kwargs)
    """
    )
    return ast.parse(source).body[0]


def create_pydantic_dataclass_to_json_data_method() -> FunctionDef:
    source = inspect.cleandoc(
        """
    def to_json_data(self, **kwargs) -> Any:
        return self.__pydantic_serializer__.to_python(**kwargs)
    """
    )
    return ast.parse(source).body[0]


def create_to_json_data_method(
    properties: list[AnnAssign | str],
    initial_value: dict | None = None,
) -> FunctionDef:
    initial_value = initial_value or {}

    def create_safe_assign_directive(
        property: AnnAssign | str,
    ) -> str:
        if isinstance(property, AnnAssign):
            key = property.target.id
            return (
                f"    if self.{key} is not None:\n"
                f"        data['{key}'] = _to_json_data(self.{key})\n"
            )
        else:
            return property

    assigns = "".join(pipe(properties, map(create_safe_assign_directive)))
    source = (
        "def to_json_data(self) -> Any:\n"
        f"    data: dict[str, Any] = {initial_value}\n"
        f"{assigns}"
        "    return data\n"
    )
    return ast.parse(source).body[0]


def create_discriminator_base_to_json_data_method() -> FunctionDef:
    source = inspect.cleandoc(
        """
    def to_json_data(self) -> Any:
        pass
    """
    )
    return ast.parse(source).body[0]


def format_property_name(format: str, property: AnnAssign):
    property.target.id = caseconverter(format, property.target.id)
    return property


def get_class_bases(class_: ClassDef) -> list[str]:
    return pipe(
        class_.bases,
        map(lambda base: base.id),
        list,
    )


def inherit(name: str, class_: ClassDef) -> ClassDef:
    class_.bases.append(Name(id=name, ctx=Load()))
    return class_


def is_enum_class(node: Any) -> bool:
    return isinstance(node, ClassDef) and "Enum" in get_class_bases(node)


def is_json_codec_method(node: Any) -> bool:
    return isinstance(node, FunctionDef) and node.name in [
        "from_json_data",
        "to_json_data",
    ]


def remove_dataclass_decorator(decorator_list: list[Name]):
    return find(lambda node: node.id != "dataclass", decorator_list)


def remove_dataclass_imports(importfroms: list[ImportFrom]):
    return find(lambda node: node.module != "dataclasses", importfroms)


def remove_json_codec_helpers(nodes: list[ast.stmt]):
    return find(
        lambda node: isinstance(node, FunctionDef)
        and node.name
        not in [
            "_from_json_data",
            "_to_json_data",
            "_parse_rfc3339",
        ],
        nodes,
    )


def remove_json_codec_methods(nodes: list[ast.stmt]):
    return find(complement(is_json_codec_method), nodes)


NodeType = TypeVar("NodeType")


def select_nodes_by_type(type: Type[NodeType], nodes: list[Any]) -> list[NodeType]:
    return find(lambda node: isinstance(node, type), nodes)


def use_implementation_type(annotation: str) -> str:
    return pipe(
        annotation,
        replace("Dict", "dict"),
        replace("Any", "object"),
        replace("List", "list"),
    )
