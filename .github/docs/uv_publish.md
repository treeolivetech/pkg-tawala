# uv Publishing Guide

Publish to [PyPI](https://pypi.org/) or [TestPyPI](https://test.pypi.org/) using [uv](https://docs.astral.sh/uv/guides/package/) and GitHub Actions Trusted Publishing.

## One-Time Setup

Use OIDC Trusted Publishing (no API tokens).

1. In GitHub repository settings, create environments:
   - `pypi`
   - `testpypi`
2. In both PyPI and TestPyPI project settings, add a trusted publisher:
   - Publisher Type: GitHub
   - Owner: `<personal account / organization username>`
   - Repository: `<repo name>`
   - Workflow: `uv_publish.yaml` (or blank to allow all workflows)
   - Environment: `pypi` for PyPI, `testpypi` for TestPyPI

## Release Workflow

The source of truth is `project.version` in `pyproject.toml`.

### 1. Set the Version

```bash
uv version --bump patch
uv version --bump minor
uv version --bump major --bump dev
uv version 2.0.0
```

Then commit and push:

```bash
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"
git push
```

### 2. Publish

The workflow is defined in `.github/workflows/uv_publish.yaml`.

#### Manual publish (Actions UI)

Run **uv Publish to PyPI or TestPyPI** and choose `pypi` or `testpypi`.

Behavior on manual dispatch:

- Reads `pyproject.toml` version and computes `v<version>`.
- Rejects development versions (any version containing `.dev`) and exits before tagging/publishing.
- Creates and pushes the tag only if it does not already exist on `origin`.
- Builds and publishes in the same run.

Use this path for TestPyPI validation before publishing to PyPI.

#### Tag-triggered publish

Pushing a tag matching `v*.*.*` triggers publish (default environment: `pypi`).
Tags matching `v*.*.*.dev*` are ignored.

Helper script (run from repository root):

```bash
uv run .github/triggers/uv_publish.py
```

The script fetches/prunes tags, reads the version, creates `v<version>`, and pushes it.

## Verify

- PyPI: `https://pypi.org/project/<package_name>/`
- TestPyPI: `https://test.pypi.org/project/<package_name>/`

Test install from TestPyPI:

```bash
uv pip install -i https://test.pypi.org/simple/ package_name
```
