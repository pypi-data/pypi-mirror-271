from functools import reduce
from deepmerge import always_merger
from jtd_codebuild.component import Component


class InheritanceResolver(Component):
    def resolve(self, schema: dict) -> dict:
        def resolve_inheritance_recursively(
            schema: dict,
            name: str,
            definition: dict,
        ) -> dict:
            """Resolve inheritance recursively.

            Args:
                schema: The schema to resolve inheritance for.
                name: The name of the definition to resolve inheritance for.
                definition: The definition to resolve inheritance for.

            Returns:
                The definition with inheritance resolved.
            """
            if "extends" not in definition:
                return definition

            # We reverse the order of the inherited defnames
            # as we want to follow python like module resolution order
            inherited_definitions = reversed(
                definition["extends"]
                if isinstance(definition["extends"], list)
                else [definition["extends"]]
            )

            # Resolve inheritance for each inherited definition
            inherited_definitions = [
                resolve_inheritance_recursively(
                    schema,
                    inherited_definition,
                    schema["definitions"][inherited_definition],
                )
                for inherited_definition in inherited_definitions
            ]

            # Merge the inherited definitions into the definition
            merged_definition = reduce(
                always_merger.merge,
                inherited_definitions,
                definition,
            )

            # Update the definition in the schema
            schema["definitions"][name] = merged_definition

            # Delete extends key from the definition
            schema["definitions"][name].pop("extends", None)

            # Return the merged definition
            return merged_definition

        for name, definition in schema["definitions"].items():
            if "extends" in definition:
                resolve_inheritance_recursively(schema, name, definition)

        return schema
