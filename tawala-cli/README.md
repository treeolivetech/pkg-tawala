# tawala-cli

Scaffold a new Tawala project in seconds.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended)

## Quick Start

Run directly without installing:

```bash
uvx tawala-cli new --project my-new-app
```

## Commands

Show CLI help:

```bash
tawala-cli -h
```

Show version:

```bash
tawala-cli -v
tawala-cli new -v
```

Initialize a project:

```bash
tawala-cli new --project <project_name> [--preset {default,vercel}] [--db {sqlite,postgresql}] [--pg_use_vars] [--layout {base,wip}]
```

## Examples

Default project (SQLite + base layout):

```bash
tawala-cli new --project my-app
```

Vercel-focused scaffold:

```bash
tawala-cli new --project my-app --preset vercel
```

PostgreSQL + environment variable configuration + WIP layout:

```bash
tawala-cli new --project my-app --db postgresql --pg_use_vars --layout wip
```

Initialize in the current directory:

```bash
tawala-cli new --project .
```

## Notes

- `--preset vercel` forces PostgreSQL and environment-variable based database configuration.
- `--pg_use_vars` is valid only when `--db postgresql` is selected.

## License

[MIT](LICENSE)
