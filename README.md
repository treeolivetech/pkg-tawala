# pkg-tawala

Monorepo for the Tawala ecosystem by Treeolive Technologies.

## Packages

| Package                                | Description                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------- |
| [`tawala`](tawala/README.md)           | Core framework package for building and running Tawala-powered Django apps. |
| [`tawala-cli`](tawala-cli/README.md)   | Project scaffolding CLI (`tawala-cli`).                                     |
| [`tawala-docs`](tawala-docs/README.md) | Documentation and demo site project.                                        |

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Quick Start (Monorepo)

```bash
uv sync --all-packages
uv run --package tawala-cli tawala-cli -h
```

## Common Workflows

Scaffold a new project:

```bash
uv run tawala-cli new --project my-new-app
```

Run the docs/demo app locally:

```bash
cd tawala-docs
uv run tawala migrate
uv run tawala runserver
```

Inspect build/install command pipelines used by Tawala:

```bash
cd tawala-docs
uv run tawala runinstall --dry
uv run tawala runbuild --dry
```

## License

[MIT](LICENSE)
