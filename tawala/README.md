# tawala

Build and deploy Django apps with confidence.

`tawala` is the core framework package that provides:

- Django settings and app wiring for Tawala projects
- A project runtime command (`tawala`) with Django management subcommands
- Additional commands such as `runserver`, `runinstall`, and `runbuild`

## Requirements

- Python 3.14+
- A valid Tawala project configuration in `pyproject.toml` under `[tool.tawala]`

## Install

With uv:

```bash
uv add tawala
```

With pip:

```bash
pip install tawala
```

## Quick Start

Scaffold a new project with the CLI:

```bash
uvx tawala-cli new my-new-project
cd my-new-project
uv sync
uv run tawala migrate
uv run tawala runserver
```

## Core Commands

Show all available commands:

```bash
tawala --help
```

Run development server:

```bash
tawala runserver
```

Run configured install/build pipelines:

```bash
tawala runinstall --dry
tawala runbuild --dry
```

## Optional Extras

PostgreSQL support:

```bash
uv add "tawala[psycopg]"
```

Vercel tooling support:

```bash
uv add "tawala[vercel]"
```

## Related Packages

- [`tawala-cli`](../tawala-cli/README.md)
- [`tawala-docs`](../tawala-docs/README.md)

## License

[MIT](LICENSE)
