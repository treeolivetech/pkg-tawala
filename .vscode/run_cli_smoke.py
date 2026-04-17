"""Run tawala-cli smoke commands for VS Code launch profiles."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _workspace_root() -> Path:
    """Return the repository workspace root from this script location."""
    return Path(__file__).resolve().parents[1]


def _resolve_generate_targets() -> tuple[str, ...]:
    """Resolve generate target choices directly from the GenerateCommand parser."""
    tawala_cli_src = _workspace_root() / "tawala-cli" / "src"
    sys.path.insert(0, str(tawala_cli_src))

    from tawala_cli.commands import GenerateCommand

    parser = argparse.ArgumentParser(add_help=False)
    GenerateCommand().add_arguments(parser)

    for action in parser._actions:
        if action.dest == "target" and action.choices:
            return tuple(str(choice) for choice in action.choices)

    raise RuntimeError("Unable to resolve generate target choices from GenerateCommand")


GENERATE_TARGETS: tuple[str, ...] = _resolve_generate_targets()


def _remove_path(path: Path) -> None:
    """Remove a file or folder if it exists."""
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _run_cli(tmp_dir: Path, args: list[str], cwd: Path | None = None) -> int:
    """Execute uv run tawala-cli with the provided arguments."""
    effective_cwd = cwd or tmp_dir
    cmd = ["uv", "run", "tawala-cli", *args]
    print(f">>> {' '.join(cmd)} (cwd={effective_cwd})")
    return subprocess.run(cmd, cwd=effective_cwd, check=False).returncode


def _run_new_default(tmp_dir: Path) -> int:
    target = tmp_dir / "launch-new-default"
    _remove_path(target)
    return _run_cli(tmp_dir, ["new", "launch-new-default"])


def _run_new_vercel(tmp_dir: Path) -> int:
    target = tmp_dir / "launch-new-vercel"
    _remove_path(target)
    return _run_cli(tmp_dir, ["new", "launch-new-vercel", "--preset", "vercel"])


def _run_new_postgres_vars_wip(tmp_dir: Path) -> int:
    target = tmp_dir / "launch-new-postgres-vars-wip"
    _remove_path(target)
    return _run_cli(
        tmp_dir,
        [
            "new",
            "launch-new-postgres-vars-wip",
            "--db",
            "postgresql",
            "--pg_use_vars",
            "--layout",
            "wip",
        ],
    )


def _run_new_dot(tmp_dir: Path) -> int:
    target = tmp_dir / "new-dot"
    _remove_path(target)
    target.mkdir(parents=True, exist_ok=True)
    return _run_cli(target, ["new", "."], cwd=target)


def _run_generate_pick(tmp_dir: Path, target: str) -> int:
    out_dir = tmp_dir / "generate" / f"out-{target}"
    _remove_path(out_dir)
    return _run_cli(
        tmp_dir,
        [
            "generate",
            target,
            "--output-dir",
            str(out_dir),
            "--project-name",
            f"gen-{target}",
        ],
    )


def _run_generate_all(tmp_dir: Path) -> int:
    _remove_path(tmp_dir / "generate")
    for target in GENERATE_TARGETS:
        code = _run_generate_pick(tmp_dir, target)
        if code != 0:
            return code
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run tawala-cli smoke launch commands")
    parser.add_argument(
        "--tmp-dir",
        default=".tmp",
        help="Temporary workspace directory used by smoke runs.",
    )

    subparsers = parser.add_subparsers(dest="mode", required=True)
    subparsers.add_parser("new-default")
    subparsers.add_parser("new-vercel")
    subparsers.add_parser("new-postgres-vars-wip")
    subparsers.add_parser("new-dot")

    pick = subparsers.add_parser("generate-pick")
    pick.add_argument("--target", choices=GENERATE_TARGETS, required=True)

    subparsers.add_parser("generate-all")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    workspace_root = _workspace_root()
    tmp_dir = (workspace_root / args.tmp_dir).resolve()
    tmp_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "new-default":
        return _run_new_default(tmp_dir)
    if args.mode == "new-vercel":
        return _run_new_vercel(tmp_dir)
    if args.mode == "new-postgres-vars-wip":
        return _run_new_postgres_vars_wip(tmp_dir)
    if args.mode == "new-dot":
        return _run_new_dot(tmp_dir)
    if args.mode == "generate-pick":
        return _run_generate_pick(tmp_dir, args.target)
    if args.mode == "generate-all":
        return _run_generate_all(tmp_dir)

    parser.error(f"Unsupported mode: {args.mode}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
