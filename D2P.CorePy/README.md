# d2p-core-py

Python wrapper for the **D2P.Core** .NET library, designed for use inside **Rhino 8 / Grasshopper** or using **Rhino.Inside CPython** outside Rhino.

The distribution is named `d2p-core-py`; the import name is `d2p_core`.

## Installation

### Inside Rhino 8 / Grasshopper

Rhino already provides the CLR (`pythonnet`), so install the package with no extras — it declares no runtime dependencies and will not pull a second `pythonnet` into Rhino's Python environment:

```python
# r: d2p-core-py
```

Or from a shell:

```bash
pip install d2p-core-py
```

### Outside Rhino (standalone CPython)

Use the `standalone` extra to install [`rhinoinside`](https://github.com/mcneel/rhino.inside-cpython), which bootstraps the Rhino runtime (and brings in `pythonnet` transitively):

```bash
pip install "d2p-core-py[standalone]"
```

`D2P.Core.dll` is bundled in `src/d2p_core/lib/` and included in every install, so the package works without the Grasshopper plugin. See [DLL Loading](#dll-loading).

### From a local clone (development)

```bash
cd D2P.CorePy
pip install -e ".[dev]"
```

The `dev` extra installs `rhinoinside`, `pytest`, `flake8`, `build`, and `twine`.

## Quick Start

```python
from d2p_core import Settings, ComponentType, GHComponent
from d2p_core import utility

# Settings is a static class — access properties directly
print(Settings.RootLayerName)       # 'D2P'
Settings.RootLayerName = 'MyRoot'   # writable properties

# Create a component type
ct = ComponentType('AB', 'AnchorBolt', LabelSize=2.5)

# Find existing components in the active document
from d2p_core.utility.instantiation import instances_by_type
from d2p_core import FilterOptions

components = instances_by_type('AB', FilterOptions())
for comp in components:
    print(comp.Name, comp.Plane)
```

## API Overview

### Core Classes

All wrapper classes use PascalCase property names matching D2P.Core.
Properties are delegated to the underlying .NET object via `__getattr__`,
so every .NET property is automatically available.

| Class | Wraps | Description |
|-------|-------|-------------|
| `ComponentBase` | `D2P.Core.Interfaces.IComponentBase` | General wrapper for any component returned from utility functions |
| `Component` | `D2P.Core.Components.Component` | Generic fallback component for documents with no registered type |
| `GHComponent` | `D2P.Core.Platforms.GHComponent` | Grasshopper component — use to **create new** components |
| `ComponentType` | `D2P.Core.Components.ComponentType` | Defines component type metadata (type ID, name, label size, color) |
| `ComponentTable` | `D2P.Core.Components.ComponentTable` | Static registry mapping type IDs to .NET component types |
| `Member` | `D2P.Core.Components.Member.Member` | Member geometry with layer info, attributes, and sub-members |
| `Settings` | `D2P.Core.Components.Settings` | Static configuration: root layer, delimiters, dimension style, tolerances |
| `LayerInfo` | `D2P.Core.Components.LayerInfo` | Layer name and color pair |
| `FilterOptions` | `D2P.Core.FilterOptions` | Regex pattern and reverse flag for filtering |

### Accessing .NET Properties

All D2P.Core PascalCase properties work directly:

```python
# Settings is static — no instantiation needed
print(Settings.RootLayerName)
print(Settings.TypeDelimiter)
Settings.RootLayerName = 'MyRoot'

# GHComponent wraps D2P.Core.Platforms.GHComponent
comp = GHComponent(ct, 'MyPart', plane)
print(comp.Name, comp.TypeId, comp.Plane)
```

### Passing to .NET Methods

The utility modules handle unwrapping automatically:

```python
from d2p_core import utility

utility.layers.create_root_layer()
utility.rhdoc.update_component_layer_colors([comp])
```

For direct .NET calls outside the utility wrappers, access `.NetObj`:

```python
some_dotnet_method(comp.NetObj)
```

### Utility Modules

Access via `d2p_core.utility.<module>`:

| Module | Wraps | Key Functions |
|--------|-------|---------------|
| `components` | `D2P.Core.Utility.Components` | `get_parent_component`, `get_child_components`, `get_joint_components`, `get_component_types` |
| `instantiation` | `D2P.Core.Utility.Instantiation` | `instances_by_name`, `instances_by_type`, `instance_from_group`, `instance_from_object` |
| `io` | `D2P.Core.Utility.IO` | `export_with_headless`, `export_components_with_headless` |
| `layers` | `D2P.Core.Utility.Layers` | `find_layer`, `create_root_layer`, `get_component_layers`, `compose_*`, `decompose_*` |
| `members` | `D2P.Core.Utility.Members` | `find_members`, `get_all_member_geometries`, `member_from_layer`, `is_component_label` |
| `objects` | `D2P.Core.Utility.Objects` | `objects_by_layer`, `objects_by_name`, `delete_component`, `get_component_type_from_object` |
| `rhdoc` | `D2P.Core.Utility.RHDoc` | `purge`, `update_component_layer_colors` |

### Type Conversions

Constructor arguments accept Python-friendly types where convenient:

| Python | .NET |
|--------|------|
| `(R, G, B)` or `(R, G, B, A)` tuple | `System.Drawing.Color` |
| `str` (GUID string) | `System.Guid` |

Conversion utility functions are available in `d2p_core._type_utils`:

- `to_net_color()` / `from_net_color()`
- `to_net_guid()` / `from_net_guid()`
- `to_python_list()` / `to_python_dict()`

All parameters also accept the raw .NET types directly.

RhinoCommon types (`Plane`, `GeometryBase`, `RhinoDoc`, etc.) are always passed through as-is.

## Committing to the document

`Commit()` takes a `delete_existing` flag, which removes objects of other components sharing the same name before adding the new ones. Pass `False` when committing into a headless document:

```python
comp.Commit()                      # replace existing objects
comp.Commit(delete_existing=False) # add without deleting
```

## DLL Loading

The package bundles `D2P.Core.dll`, so it works with or without the D2P Grasshopper plugin installed.

On import it looks for an already-loaded `D2P.Core` assembly:

- **Found** (the Grasshopper plugin loaded it): that assembly is used. It cannot be replaced once loaded, so it always takes precedence over the bundled copy.
- **Not found**: the bundled DLL is loaded from `d2p_core/lib/`.

When a host assembly is used and it is not byte-identical to the bundled one, the package checks it:

- Differing assembly versions produce a `UserWarning` naming both versions and the path the assembly was loaded from.
- A host assembly missing API this wrapper needs raises a `RuntimeError` explaining that the installed plugin is older than the package. Set `D2P_ALLOW_INCOMPATIBLE_DLL=1` to downgrade it to a warning.

`D2P.Core.csproj` currently does not stamp an assembly version — every build reports `0.0.0.0` — so version comparison is skipped until it does, and the API probe carries the check on its own.

Inspect what was resolved with:

```python
import d2p_core
print(d2p_core.assembly_info())
# {'source': 'host', 'path': 'C:\\...\\D2P.GHPlugin\\D2P.Core.dll',
#  'version': '0.0.0.0', 'bundled_path': '...', 'bundled_version': '0.0.0.0',
#  'in_rhino': True, 'package_version': '0.1.0'}
```

When running **outside Rhino** (e.g. in a standalone script or test suite), the package uses [`rhinoinside`](https://pypi.org/project/rhinoinside/) to bootstrap a full Rhino runtime. Install the `standalone` or `dev` extra, or `pip install rhinoinside` directly. Set `D2P_RHINO_SYSTEM_PATH` if Rhino is not at the default location.

## License

MIT — see [LICENSE](LICENSE).
