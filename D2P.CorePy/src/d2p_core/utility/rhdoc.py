from __future__ import annotations

from D2P.Core.Utility import RHDoc as _NetRHDoc

from d2p_core._type_utils import _unwrap


def purge(doc) -> None:
    """Remove empty layers from a Rhino document."""
    _NetRHDoc.Purge(doc)


def update_component_layer_colors(components) -> None:
    """Update layer colors for a collection of components.

    Groups by TypeId and updates both the type root layer
    and sublayer colors.
    """
    _NetRHDoc.UpdateComponentLayerColors(
        [_unwrap(c) for c in components]
    )
