from __future__ import annotations

from D2P.Core.Utility import Layers as _NetLayers

from d2p_core._type_utils import _unwrap


# --- Create ---

def create_layer_for_component(component):
    """Create the type layer for a component. Returns a Layer."""
    return _NetLayers.CreateLayer(_unwrap(component))


def create_layer_for_member(member):
    """Create the layer hierarchy for a member. Returns a Layer."""
    return _NetLayers.CreateLayer(_unwrap(member))


def create_root_layer():
    """Create or find the D2P root layer. Returns a Layer."""
    return _NetLayers.CreateRootLayer()


def create_component_type_layer(component):
    """Create the component type layer for a component. Returns a Layer."""
    return _NetLayers.CreateComponentTypeLayer(_unwrap(component))


# --- Find ---

def find_root_layer():
    """Find the D2P root layer.

    Returns (root_layer, found) where found is bool.
    """
    result, root_layer = _NetLayers.FindRootLayer()
    return root_layer, result


def find_layer(member):
    """Find a layer for a member. Returns the Layer or None."""
    return _NetLayers.FindLayer(_unwrap(member))


def find_layer_with_count(member):
    """Find a layer for a member.

    Returns (layer, layers_found).
    """
    layer, layers_found = _NetLayers.FindLayer(
        _unwrap(member)
    )
    return layer, int(layers_found)


def find_layer_by_index(layer_index: int):
    """Find a layer by its index."""
    return _NetLayers.FindLayer(layer_index)


def find_component_layer_by_type(type_id: str):
    """Find a component layer by its type ID."""
    return _NetLayers.FindComponentLayerByType(type_id)


def find_layer_by_name(
    layer_name: str,
    include_referenced: bool = False,
):
    """Find a layer by name under the root layer."""
    return _NetLayers.FindLayerByName(
        layer_name, include_referenced,
    )


def find_component_type_root_layers() -> list:
    """Find all component type root layers."""
    return list(_NetLayers.FindComponentTypeRootLayers())


def find_component_type_root_layer_from_object(obj):
    """Find the component type root layer from a RhinoObject."""
    return _NetLayers.FindComponentTypeRootLayer(obj)


def find_component_type_root_layer(component):
    """Find the component type root layer for a component."""
    return _NetLayers.FindComponentTypeRootLayer(
        _unwrap(component)
    )


# --- Layer Validation ---

def is_component_type_root_layer(component_or_layer, layer_name=None) -> bool:
    """Check if a layer is a component type root layer.

    Can be called as::

        is_component_type_root_layer(component, layer_name)
        is_component_type_root_layer(layer)
    """
    if layer_name is not None:
        return bool(
            _NetLayers.IsComponentTypeRootLayer(
                _unwrap(component_or_layer), layer_name,
            )
        )
    return bool(
        _NetLayers.IsComponentTypeRootLayer(component_or_layer)
    )


# --- Compose / Decompose ---

def compose_component_layer_name(
    component, raw_layer_name: str,
) -> str:
    """Compose a component sub-layer name."""
    return str(
        _NetLayers.ComposeComponentLayerName(
            _unwrap(component), raw_layer_name
        )
    )


def compose_component_type_layer_name(
    component_type_or_type_id,
    description: str | None = None,
) -> str:
    """Compose a component type root layer name.

    Can be called as::

        compose_component_type_layer_name(component_type)
        compose_component_type_layer_name('AB', 'SomeType')
    """
    unwrapped = _unwrap(component_type_or_type_id)
    if isinstance(unwrapped, str):
        return str(
            _NetLayers.ComposeComponentTypeLayerName(
                unwrapped, description or '',
            )
        )
    return str(
        _NetLayers.ComposeComponentTypeLayerName(unwrapped)
    )


def compose_full_layer_path(member) -> str:
    """Compose the full layer path for a member."""
    return str(
        _NetLayers.ComposeFullLayerPath(_unwrap(member))
    )


def compose_member_layer_name(member) -> str:
    """Compose the member layer name (recursive via parent)."""
    return str(
        _NetLayers.ComposeMemberLayerName(_unwrap(member))
    )


def decompose_layer_name(
    component, layer_name: str,
) -> str:
    """Extract the suffix portion of a layer name."""
    return str(
        _NetLayers.DecomposeLayerName(
            _unwrap(component), layer_name
        )
    )


# --- Get Layer Info ---

def get_layer_info(layer):
    """Get a LayerInfo from a Rhino Layer."""
    return _NetLayers.GetLayerInfo(layer)


def get_raw_layer_name(layer) -> str:
    """Get the raw layer name from a Layer."""
    return str(_NetLayers.GetRawLayerName(layer))


# --- Get Component Info from Layer ---

def get_component_type_id(layer) -> str:
    """Extract the type ID from a component type layer."""
    return str(_NetLayers.GetComponentTypeID(layer))


def get_component_type_name(layer_or_obj) -> str:
    """Extract the type name from a layer or RhinoObject."""
    return str(_NetLayers.GetComponentTypeName(layer_or_obj))


def get_component_type_label_size(component_layer) -> float:
    """Get the label text height for a component type."""
    return float(
        _NetLayers.GetComponentTypeLabelSize(component_layer)
    )


# --- Traversal ---

def get_component_layers(component) -> list:
    """Get all layers belonging to a component type."""
    return list(
        _NetLayers.GetComponentLayers(_unwrap(component))
    )


def get_ancestor_layers(
    layer, include_root: bool = False,
) -> list:
    """Get ancestor layers of a given layer."""
    return list(
        _NetLayers.GetAncestorLayers(layer, include_root)
    )


def get_child_layers(layer_or_index) -> list:
    """Get child layers of a given layer or layer index."""
    return list(_NetLayers.GetChildLayers(layer_or_index))


def get_child_layer_indices(layer_idx: int) -> list[int]:
    """Get child layer indices for a layer index."""
    return list(_NetLayers.GetChildLayerIndices(layer_idx))
