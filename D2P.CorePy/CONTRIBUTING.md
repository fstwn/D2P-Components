# Contributing to d2p-core-py

This document covers development setup, building the bundled `D2P.Core.dll`,
running tests, and publishing releases to PyPI.

For Grasshopper plugin (C# / `.gha`) development, see
[CONTRIBUTION.md](../CONTRIBUTION.md) in the repository root.

## Prerequisites

| Tool | Purpose |
|------|---------|
| [.NET SDK](https://dotnet.microsoft.com/download) | Build `D2P.Core.dll` (target: **net7.0**) |
| [Rhino 8](https://www.rhino3d.com/download/) | Runtime for tests outside Rhino (via Rhino.Inside) |
| Python **3.9+** | Wrapper and test suite |

Rhino must be installed at the default path or exposed via
`D2P_RHINO_SYSTEM_PATH` pointing at the Rhino `System` directory, e.g.
`C:\Program Files\Rhino 8\System`.

## Development setup

All commands below assume the repository root and run from `D2P.CorePy/`.

### Option A — conda (recommended on Windows)

```bash
cd D2P.CorePy
conda env create -f environment.yml
conda activate d2p_core_dev
```

The environment installs the package editable with the `dev` extras
(`rhinoinside`, `pytest`, `flake8`, `build`, `twine`).

To refresh after pulling changes:

```bash
conda activate d2p_core_dev
pip install -e ".[dev]"
```

### Option B — pip / venv

```bash
cd D2P.CorePy
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
```

## Refresh the bundled DLL

The wheel ships `D2P.Core.dll` at `src/d2p_core/lib/D2P.Core.dll`. Update
it whenever the C# API in `../D2P.Core/` changes, **before** building a
release.

From the repository root:

```bash
dotnet build D2P.Core/D2P.Core.csproj -c Release -f net7.0
```

Then copy the output (paths relative to `D2P.CorePy/`):

```bash
copy ..\D2P.Core\bin\Release\net7.0\D2P.Core.dll src\d2p_core\lib\D2P.Core.dll
```

On macOS/Linux:

```bash
cp ../D2P.Core/bin/Release/net7.0/D2P.Core.dll src/d2p_core/lib/D2P.Core.dll
```

Verify the wrapper still matches the DLL:

```bash
pytest tests/test_runtime.py::test_bundled_dll_satisfies_required_api -q
```

See also [src/d2p_core/lib/README.md](src/d2p_core/lib/README.md) for how
the bundled DLL interacts with an already-loaded plugin assembly.

## Lint and test

Use the environment's Python directly — `conda run` can hang on teardown
when Rhino.Inside shuts down:

```bash
python -m flake8 src tests
python -m pytest
```

Integration tests load Rhino via `rhinoinside` on import. A
`System.AccessViolationException` from Rhino's licensing thread **after**
tests reach 100% is a known Rhino.Inside shutdown issue, not a test failure.

## Build distribution artifacts

Clean previous outputs, then build wheel and sdist:

```bash
cd D2P.CorePy
rm -rf dist build                    # omit on Windows if absent
python -m build
python -m twine check dist/*
```

Expected artifacts in `dist/`:

- `d2p_core_py-<version>-py3-none-any.whl` — includes `d2p_core/lib/D2P.Core.dll`
- `d2p_core_py-<version>.tar.gz`

Do not commit `dist/`, `build/`, or `*.egg-info/` — they are gitignored.

## Publish to PyPI

### Credentials

Create an API token at https://pypi.org/manage/account/token/ and store it
in `~/.pypirc` (on Windows: `C:\Users\<you>\.pypirc`):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxx
```

Never commit `.pypirc` or tokens to git.

### Upload

Test on TestPyPI first:

```bash
python -m twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --no-deps d2p-core-py
```

Then upload to PyPI:

```bash
python -m twine upload dist/*
```

PyPI metadata is fixed per release — correcting author fields or README
requires bumping the version and uploading again.

## Release checklist

1. Merge C# changes and refresh `src/d2p_core/lib/D2P.Core.dll` (see above).
2. Adapt Python wrappers if the C# API changed.
3. Bump `[project].version` in [pyproject.toml](pyproject.toml).
4. Optionally sync `_FALLBACK_VERSION` in
   [src/d2p_core/_runtime.py](src/d2p_core/_runtime.py) for editable installs
   without distribution metadata.
5. Run `flake8` and `pytest`.
6. `python -m build` and `python -m twine check dist/*`.
7. Upload with `twine` (TestPyPI, then PyPI).
8. Tag the release in git if your workflow uses tags.

## Project layout

```
D2P.CorePy/
├── pyproject.toml          # package metadata and version
├── MANIFEST.in             # sdist file inclusion (DLL, LICENSE, tests)
├── environment.yml         # conda dev environment
├── src/d2p_core/           # importable package
│   ├── lib/D2P.Core.dll    # bundled .NET assembly
│   └── utility/            # Python wrappers for D2P.Core.Utility.*
└── tests/
```

Distribution name on PyPI: **`d2p-core-py`**. Import name: **`d2p_core`**.
