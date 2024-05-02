# JSON Type Definition Code Build

[![PyPI version](https://badge.fury.io/py/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild)
[![Testsuite](https://github.com/01Joseph-Hwang10/jtd-codebuild/workflows/Test%20and%20Lint/badge.svg)](https://github.com/01Joseph-Hwang10/jtd-codebuild/actions?query=workflow%3A"Test+and+Lint")
[![Python version](https://img.shields.io/pypi/pyversions/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild)
[![Project Status](https://img.shields.io/pypi/status/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild/)
[![Supported Interpreters](https://img.shields.io/pypi/implementation/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild/)
[![License](https://img.shields.io/pypi/l/jtd-codebuild.svg)](https://github.com/pawelzny/jtd-codebuild/blob/master/LICENSE)

jtd-codebuild is a tool for generating language specific schemas and interfaces code from JSON Type Definition IDL files in either yaml or json format.

This tool is built on top of [jtd-codegen](https://jsontypedef.com/docs/jtd-codegen/) so check out the documentation if you don't have a clue about JSON Type Definition.

## Quick Example

In this example, we will generate Python and TypeScript code from JSON Type Definition IDL files.

First, copy and paste the following configuration file to the root of your project.

```json
{
  "include": [
    "src"
  ],
  "references": [],
  "jtdBundlePath": "gen/schema.jtd.json",
  "targets": [
    {
      "language": "python",
      "path": "gen/python"
    },
    {
      "language": "typescript",
      "path": "gen/typescript"
    }
  ],
  "$schema": "https://raw.githubusercontent.com/01Joseph-Hwang10/jtd-codebuild/master/jtd_codebuild/config/project/config.json"
}
```

Then, we'll create some JSON Type Definition IDL files in the `src` directory.

```yaml
# src/book.jtd.yaml
Book:
  properties:
    id:
      type: string
    title:
      type: string
```
```yaml
# src/user.jtd.yaml
User:
  properties:
    id:
      type: string
    name:
      type: string
    books:
      elements:
        ref: Book
```

Finally, run the following command to generate the code.

```bash
jtd-codebuild .
```

You can find the generated code in the `gen` directory.

## More Examples

You can find more examples under the [tests] directory:

- [Python Codegen Examples][python-codegen-example]
- [TypeScript Codegen Examples][typescript-codegen-example]
- [Monorepo Example (includes other languages' examples)][monorepo-example]

## API Documentation

See the [API Documentation](./docs/index.md) for more information.

## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/jtd-codebuild/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/jtd-codebuild/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`jtd-codebuild` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/jtd-codebuild/blob/master/LICENSE).

[python-codegen-example]: ./tests/python_targets/project/
[typescript-codegen-example]: ./tests/typescript_targets/project/
[monorepo-example]: ./tests/monorepo/workspace/
[tests]: ./tests/
