"""Cleanup .mock directories for CLI task testing."""

import pathlib
import shutil
import sys


def cleanup_mock_directory(target: str, recreate: bool = False) -> None:
    """Clean up or reset a .mock directory.
    
    Args:
        target: The name of the subdirectory within '.mock' to clean up.
        recreate: If True, recreate the directory after removal.
    
    Raises:
        ValueError: If target is empty or contains invalid path components.
    """
    if not target or "/" in target or "\\" in target or target == "..":
        raise ValueError(f"Invalid target directory name: {target}")
    
    mock_dir = pathlib.Path(".mock")
    mock_dir.mkdir(parents=True, exist_ok=True)
    
    target_dir = mock_dir / target
    shutil.rmtree(target_dir, ignore_errors=True)
    
    if recreate:
        target_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cleanup_mock.py <target> [--recreate]", file=sys.stderr)
        sys.exit(1)
    
    target = sys.argv[1]
    recreate = "--recreate" in sys.argv
    
    try:
        cleanup_mock_directory(target, recreate)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
