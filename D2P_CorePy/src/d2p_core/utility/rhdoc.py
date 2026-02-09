from __future__ import annotations

from D2P_Core.Utility import RHDoc as _NetRHDoc

from d2p_core._type_utils import _unwrap, from_net_guid


def purge(doc) -> None:
    """Remove empty layers from a Rhino document."""
    _NetRHDoc.Purge(doc)


def create_headless(doc):
    """Create a headless RhinoDoc copy."""
    return _NetRHDoc.CreateHeadless(doc)


def add_to_rhino_doc(
    component, doc=None, replace_existing: bool = False,
) -> str:
    """Add a component to a Rhino document."""
    result = _NetRHDoc.AddToRhinoDoc(
        _unwrap(component), doc, replace_existing
    )
    return from_net_guid(result)


def update_component_type_layer_colors(
    component_type, doc,
) -> None:
    """Update the layer color of a component type root layer."""
    _NetRHDoc.UpdateComponentTypeLayerColors(
        _unwrap(component_type), doc
    )


def update_component_sublayer_colors(component) -> None:
    """Update sublayer colors from the staging collection."""
    _NetRHDoc.UpdateComponentSublayerColors(
        _unwrap(component)
    )
