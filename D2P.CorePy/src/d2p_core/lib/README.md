# D2P.Core.dll

This directory contains the bundled `D2P.Core.dll` shipped with `d2p-core-py`.

It is the fallback used when no D2P.Core assembly is already loaded. Inside
Rhino with the D2P Grasshopper plugin installed, the plugin's assembly is
loaded first and takes precedence; this copy is then only used for the
compatibility check reported by `d2p_core.assembly_info()`.

Refresh it whenever the C# API changes, before building a release:

```bash
dotnet build ../../../../D2P.Core/D2P.Core.csproj -c Release -f net7.0
copy ..\..\..\..\D2P.Core\bin\Release\net7.0\D2P.Core.dll .
```

Then run the test suite — `test_bundled_dll_satisfies_required_api` fails if
the wrapper binds to API this DLL does not have.

Note that `D2P.Core.csproj` sets `GenerateAssemblyInfo=False` and never
defines `AssemblyVersion`, so every build reports `0.0.0.0`. Until a version
is stamped there, `_runtime.py` cannot compare versions and falls back to
probing for required types and members.
