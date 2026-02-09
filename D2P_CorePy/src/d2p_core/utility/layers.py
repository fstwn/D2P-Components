from __future__ import annotations

from D2P_Core.Utility import Layers as _NetLayers

from d2p_core._type_utils import (
    _unwrap, to_net_color, from_net_color,
    to_net_guid, from_net_guid,
)


# --- Find ---

def find_layer(component, raw_layer_name: str) -> tuple:
    """Find a layer by name. Returns (layer, layers_found)."""
    layer, layers_found = _NetLayers.FindLayer(
        _unwrap(component), raw_layer_name
    )
    return layer, int(layers_found)


def find_layer_by_index(layer_index: int, doc=None):
    """Find a layer by its index."""
    return _NetLayers.FindLayer(layer_index, doc)


def find_layer_index_by_full_path(
    component, raw_layer_name: str,
    delimiter: str = ':',
) -> int:
    """Find a layer index by traversing the full path."""
    return int(
        _NetLayers.FindLayerIndexByFullPath(
            _unwrap(component),
            raw_layer_name, delimiter,
        )
    )


def find_layer_by_full_path(
    component, raw_layer_name: str,
    delimiter: str = ':',
):
    """Find a layer by traversing the full path."""
    return _NetLayers.FindLayerByFullPath(
        _unwrap(component), raw_layer_name, delimiter
    )


def find_all_existent_component_type_root_layers(
    settings, doc=None,
) -> list:
    """Find all existing component type root layers."""
    return list(
        _NetLayers.FindAllExistentComponentTypeRootLayers(
            _unwrap(settings), doc
        )
    )


def find_component_layer_by_type(
    type_id: str, root_layer_name: str,
):
    """Find a component layer by its type ID."""
    return _NetLayers.FindComponentLayerByType(
        type_id, root_layer_name
    )


def find_layer_by_name(
    doc, layer_name: str, root_layer_name: str,
    include_referenced: bool = False,
):
    """Find a layer by name under a root layer."""
    return _NetLayers.FindLayerByName(
        doc, layer_name, root_layer_name,
        include_referenced,
    )


# --- Create ---

def create_staging_layers(component) -> list[int]:
    """Create staging layers for a component."""
    return list(
        _NetLayers.CreateStagingLayers(_unwrap(component))
    )


def create_root_layer(
    root_layer_name_or_component,
    root_layer_color=None, doc=None,
):
    """Create or find the root layer.

    Can be called as:
        create_root_layer(component, doc=doc)
        create_root_layer('D2P', (220, 75, 58), doc)
    """
    unwrapped = _unwrap(root_layer_name_or_component)
    if isinstance(unwrapped, str):
        return _NetLayers.CreateRootLayer(
            unwrapped,
            to_net_color(root_layer_color), doc,
        )
    return _NetLayers.CreateRootLayer(unwrapped, doc)


def create_component_type_layer(component):
    """Create the component type layer for a component."""
    return _NetLayers.CreateComponentTypeLayer(
        _unwrap(component)
    )


# --- Layer name composition / decomposition ---

def is_component_type_top_layer(
    component_or_layer, layer_name_or_settings=None,
) -> bool:
    """Check if a layer is the top-level component type layer.

    Can be called as:
        is_component_type_top_layer(component, layer_name)
        is_component_type_top_layer(layer, settings)
    """
    if isinstance(layer_name_or_settings, str):
        return bool(
            _NetLayers.IsComponentTypeTopLayer(
                _unwrap(component_or_layer),
                layer_name_or_settings,
            )
        )
    return bool(
        _NetLayers.IsComponentTypeTopLayer(
            component_or_layer,
            _unwrap(layer_name_or_settings),
        )
    )


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
    delimiter: str = '-',
) -> str:
    """Compose a component type root layer name.

    Can be called as:
        compose_component_type_layer_name(component_type)
        compose_component_type_layer_name('AB', 'SomeType')
    """
    unwrapped = _unwrap(component_type_or_type_id)
    if isinstance(unwrapped, str):
        return str(
            _NetLayers.ComposeComponentTypeLayerName(
                unwrapped,
                description or '', delimiter,
            )
        )
    return str(
        _NetLayers.ComposeComponentTypeLayerName(unwrapped)
    )


def compose_full_layer_path(
    layer_name: str, parent_layer_id, doc,
) -> str:
    """Compose a full layer path from name and parent ID."""
    return str(
        _NetLayers.ComposeFullLayerPath(
            layer_name, to_net_guid(parent_layer_id), doc
        )
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


# --- Get root / type layers ---

def get_root_layer(doc, root_layer_name: str):
    """Get the root layer by name."""
    return _NetLayers.GetRootLayer(doc, root_layer_name)


def get_root_layer_id(component) -> str:
    """Get the root layer GUID as a string."""
    return from_net_guid(
        _NetLayers.GetRootLayerID(_unwrap(component))
    )


def get_component_type_root_layer_from_object(
    obj, settings, doc=None,
):
    """Get the component type root layer from a RhinoObject."""
    return _NetLayers.GetComponentTypeRootLayer(
        obj, _unwrap(settings), doc
    )


def get_component_type_root_layer(
    component_type, doc=None,
):
    """Get the component type root layer."""
    return _NetLayers.GetComponentTypeRootLayer(
        _unwrap(component_type), doc
    )


def get_component_layer_id(component) -> str:
    """Get the component type layer GUID as a string."""
    return from_net_guid(
        _NetLayers.GetComponentLayerID(
            _unwrap(component)
        )
    )


# --- Get component type info from layer ---

def get_component_type_id(
    component_layer, settings,
) -> str:
    """Extract the type ID from a component type layer."""
    return str(
        _NetLayers.GetComponentTypeID(
            component_layer, _unwrap(settings)
        )
    )


def get_component_type_name(
    component_layer_or_obj, settings,
) -> str:
    """Extract the type name from a layer or RhinoObject."""
    return str(
        _NetLayers.GetComponentTypeName(
            component_layer_or_obj, _unwrap(settings)
        )
    )


def get_component_type_label_size(
    component_layer, settings,
) -> float:
    """Get the label text height for a component type."""
    return float(
        _NetLayers.GetComponentTypeLabelSize(
            component_layer, _unwrap(settings)
        )
    )


def get_component_type_settings(
    component_layer_or_obj, settings,
):
    """Get the resolved Settings for a component type."""
    return _NetLayers.GetComponentTypeSettings(
        component_layer_or_obj, _unwrap(settings)
    )


# --- Traversal ---

def get_component_layers(
    component_type,
    include_ancestor_layers: bool = False,
    doc=None,
) -> list:
    """Get all layers belonging to a component type."""
    return list(
        _NetLayers.GetComponentLayers(
            _unwrap(component_type),
            include_ancestor_layers, doc,
        )
    )


def get_ancestor_layers(
    layer, doc=None, include_root: bool = False,
) -> list:
    """Get ancestor layers of a given layer."""
    return list(
        _NetLayers.GetAncestorLayers(
            layer, doc, include_root
        )
    )


def get_child_layers(layer_or_index, doc=None) -> list:
    """Get child layers of a given layer or layer index."""
    return list(
        _NetLayers.GetChildLayers(layer_or_index, doc)
    )


def get_child_layer_indices(
    layer_idx: int, doc=None,
) -> list[int]:
    """Get child layer indices for a layer index."""
    return list(
        _NetLayers.GetChildLayerIndices(layer_idx, doc)
    )
