# D2P.Core.dll

Bundled `D2P.Core.dll` shipped inside the `d2p-core-py` wheel.

- **Fallback** when no `D2P.Core` assembly is already loaded in the process.
- **Precedence**: if the D2P Grasshopper plugin loaded its copy first, that
  assembly is used and cannot be replaced. This file is then only used for the
  compatibility check reported by `d2p_core.assembly_info()`.

Rebuild and copy instructions, tests, and release steps:
[CONTRIBUTING.md](../../../CONTRIBUTING.md) (section *Refresh the bundled DLL*).
