# d2p_core

Python wrapper for the **D2P.Core** .NET library, designed for use inside **Rhino 8 / Grasshopper** or using **Rhino.Inside CPython** (both via pythonnet).

## Installation

-> Package is not yet on PyPi yet, install from source!

### From source (development)

```
cd D2P.CorePy
pip install -e '.[dev]'
```

The `dev` extra installs [`rhinoinside`](https://github.com/mcneel/rhino.inside-cpython) (required for testing outside Rhino), `pytest`, and `flake8`.

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
| `GHComponent` | `D2P.Core.Platforms.GHComponent` | Grasshopper component — use to **create new** components |
| `ComponentType` | `D2P.Core.Components.ComponentType` | Defines component type metadata (type ID, name, label size, color) |
| `ComponentTable` | `D2P.Core.Components.ComponentTable` | Static registry mapping type IDs to .NET component types |
| `MemberGeo` | `D2P.Core.Components.Member.MemberGeo` | Member geometry with layer info, attributes, and sub-members |
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
| `objects` | `D2P.Core.Utility.Objects` | `objects_by_layer`, `delete_component`, `get_component_type_from_object` |
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

## DLL Loading

The package bundles `D2P.Core.dll`. On import, it checks whether the assembly is already loaded (e.g., via the D2P Grasshopper plugin). If so, it reuses the existing assembly and warns on version mismatch. The bundled DLL is only loaded as a fallback.

When running **outside Rhino** (e.g. in a standalone script or test suite), the package uses [`rhinoinside`](https://pypi.org/project/rhinoinside/) to bootstrap a full Rhino runtime. Install it via `pip install rhinoinside` or use the `dev` extra.

## License

MIT — see [LICENSE](LICENSE).
