# D2P.Core.dll

This directory contains the bundled `D2P.Core.dll` shipped with `d2p_core`.

When updating the Python wrapper to a new D2P.Core release, rebuild the C# project and replace this file:

```bash
dotnet build ../../D2P.Core/D2P.Core.csproj -c Release -f net7.0
copy ..\..\D2P.Core\bin\Release\net7.0\D2P.Core.dll .
```

Keep the DLL version in sync with `version` in `pyproject.toml` and `PACKAGE_VERSION` in `_runtime.py`.
