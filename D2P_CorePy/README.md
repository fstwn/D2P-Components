# d2p_core

Python wrapper for the **D2P_Core** .NET library, designed for use inside **Rhino 8 / Grasshopper** or using **Rhino.Inside CPython** (both via pythonnet).

## Installation

-> Package is not yet on PyPi yet, install from source!

### ~~Inside Rhino 8~~

~~Open the Rhino Script Editor Python shell and run:~~

~~`pip install d2p_core`~~

~~Or from a system terminal targeting Rhino's bundled Python:~~

~~`%USERPROFILE%\.rhinocode\py39-rh8\python.exe -m pip install d2p_core`~~

### From source (development)

```
cd D2P_CorePy
pip install -e '.[dev]'
```

The `dev` extra installs [`rhinoinside`](https://github.com/mcneel/rhino.inside-cpython) (required for testing outside Rhino), `pytest`, and `flake8`.

## Quick Start

```python
from d2p_core import Settings, ComponentType, Component
from d2p_core import utility

# Create settings (defaults match the C# library)
settings = Settings()

# Create a component type
ct = ComponentType('AB', 'AnchorBolt', settings, LabelSize=2.5)

# Find existing components in the active document
from d2p_core.utility.instantiation import instances_by_type
from d2p_core import FilterOptions

components = instances_by_type('AB', settings, FilterOptions())
for comp in components:
    print(comp.Name, comp.Plane)
```

## API Overview

### Core Classes

All wrapper classes use PascalCase property names matching D2P_Core.
Properties are delegated to the underlying .NET object via `__getattr__`,
so every .NET property is automatically available.

| Class | Wraps | Description |
|-------|-------|-------------|
| `Component` | `D2P_Core.Component` | Main component — holds geometry, attributes, and layer collections |
| `ComponentType` | `D2P_Core.ComponentType` | Defines component type metadata (type ID, name, label size, color) |
| `ComponentMember` | `D2P_Core.ComponentMember` | Groups geometry with layer info and attributes for adding to a component |
| `Settings` | `D2P_Core.Settings` | Configuration: root layer, delimiters, dimension style |
| `LayerInfo` | `D2P_Core.LayerInfo` | Layer name and color pair |
| `FilterOptions` | `D2P_Core.FilterOptions` | Regex pattern and reverse flag for filtering |

### Accessing .NET Properties

All D2P_Core PascalCase properties work directly:

```python
settings = Settings()
print(settings.RootLayerName)
print(settings.TypeDelimiter)
settings.RootLayerName = 'MyRoot'

comp = Component(ct, 'MyPart', plane)
print(comp.Name, comp.TypeID, comp.Plane)
```

### Passing to .NET Methods

The utility modules handle unwrapping automatically:

```python
from d2p_core import utility

utility.rhdoc.add_to_rhino_doc(comp)
utility.layers.create_root_layer(comp)
```

For direct .NET calls outside the utility wrappers, access `.NetObj`:

```python
some_dotnet_method(comp.NetObj)
```

### Utility Modules

Access via `d2p_core.utility.<module>`:

| Module | Wraps | Key Functions |
|--------|-------|---------------|
| `group` | `D2P_Core.Utility.Group` | `add_group`, `get_group_index` |
| `instantiation` | `D2P_Core.Utility.Instantiation` | `instances_by_name`, `instances_by_type`, `get_children`, `get_joints` |
| `io` | `D2P_Core.Utility.IO` | `export`, `export_with_headless` |
| `layers` | `D2P_Core.Utility.Layers` | `find_layer`, `create_root_layer`, `get_component_layers` |
| `objects` | `D2P_Core.Utility.Objects` | `objects_by_layer`, `delete_component`, `LayerScope` enum |
| `rhdoc` | `D2P_Core.Utility.RHDoc` | `add_to_rhino_doc`, `purge`, `create_headless` |

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

The package bundles `D2P_Core.dll`. On import, it checks whether the assembly is already loaded (e.g., via the D2P Grasshopper plugin). If so, it reuses the existing assembly and warns on version mismatch. The bundled DLL is only loaded as a fallback.

When running **outside Rhino** (e.g. in a standalone script or test suite), the package uses [`rhinoinside`](https://pypi.org/project/rhinoinside/) to bootstrap a full Rhino runtime. Install it via `pip install rhinoinside` or use the `dev` extra.

## License

MIT — see [LICENSE](LICENSE).
