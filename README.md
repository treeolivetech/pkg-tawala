# pkg-treeolive

Monorepo for the `treeolive` ecosystem by Treeolive Technologies.

## Packages

| Package                                    | Description                                |
| ------------------------------------------ | ------------------------------------------ |
| [`treeolive`](treeolive/README.md)         | Core framework package.                    |
| [`treeolive-api`](treeolive-api/README.md) | Project scaffolding CLI (`treeolive-api`). |

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Quick Start (Monorepo)

```bash
uv sync --all-packages
uv run --package treeolive-api treeolive-api -h
```

## Common Workflows

Scaffold a new project:

```bash
uv run treeolive-api new --project my-new-app
```

## License

[MIT](LICENSE)
