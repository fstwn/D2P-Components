from __future__ import annotations

import enum

from D2P_Core.Utility import Objects as _NetObjects

from d2p_core._type_utils import (
    _unwrap, to_net_guid, from_net_guid, from_net_color,
)


class LayerScope(enum.Enum):
    """Python equivalent of D2P_Core.Utility.Objects.LayerScope."""
    CURRENT_ONLY = 'CurrentOnly'
    INCLUDE_CHILDREN = 'IncludeChildren'


def _to_net_scope(scope: LayerScope):
    return getattr(_NetObjects.LayerScope, scope.value)


def component_type_id_from_object(
    obj, settings,
) -> str:
    """Get the component type ID from a RhinoObject."""
    return str(
        _NetObjects.ComponentTypeIDFromObject(
            obj, _unwrap(settings)
        )
    )


def component_type_name_from_object(
    obj, settings,
) -> str:
    """Get the component type name from a RhinoObject."""
    return str(
        _NetObjects.ComponentTypeNameFromObject(
            obj, _unwrap(settings)
        )
    )


def component_type_layer_color_from_object(
    obj, settings,
) -> tuple[int, int, int, int]:
    """Get the component type layer color from a RhinoObject."""
    return from_net_color(
        _NetObjects.ComponentTypeLayerColorFromObject(
            obj, _unwrap(settings)
        )
    )


def objects_by_layer_typed(
    layer_idx: int, component, scope: LayerScope,
):
    """Get typed geometry objects from a layer."""
    return list(
        _NetObjects.ObjectsByLayer[object](
            layer_idx, _unwrap(component),
            _to_net_scope(scope),
        )
    )


def objects_by_layer(
    layer_idx: int, component, scope: LayerScope,
) -> list:
    """Get GeometryBase objects from a layer."""
    return list(
        _NetObjects.ObjectsByLayer(
            layer_idx, _unwrap(component),
            _to_net_scope(scope),
        )
    )


def objects_by_layer_doc(layer, doc=None) -> list:
    """Get RhinoObjects on a layer from the document."""
    return list(_NetObjects.ObjectsByLayer(layer, doc))


def object_ids_by_layer(
    component, layer_idx: int, doc=None,
) -> list[str]:
    """Get object GUIDs on a layer for a component."""
    return [
        from_net_guid(g)
        for g in _NetObjects.ObjectIDsByLayer(
            _unwrap(component), layer_idx, doc
        )
    ]


def objects_by_group(group_idx: int, doc) -> list:
    """Get RhinoObjects in a group."""
    return list(_NetObjects.ObjectsByGroup(group_idx, doc))


def objects_by_group_on_layer(
    group_idx: int, layer, doc,
) -> list:
    """Get RhinoObjects in a group filtered to a layer."""
    return list(
        _NetObjects.ObjectsByGroup(group_idx, layer, doc)
    )


def delete_objects(component, layer=None) -> int:
    """Delete objects belonging to a component."""
    c = _unwrap(component)
    if layer is not None:
        return int(_NetObjects.DeleteObjects(c, layer))
    return int(_NetObjects.DeleteObjects(c))


def delete_component(component) -> int:
    """Delete all objects of a component including its label."""
    return int(
        _NetObjects.DeleteComponent(_unwrap(component))
    )


def delete_components(components) -> int:
    """Delete all objects of multiple components."""
    return int(
        _NetObjects.DeleteComponents(
            [_unwrap(c) for c in components]
        )
    )


def object_group_id(object_id, doc) -> int:
    """Get the single group ID for an object."""
    return int(
        _NetObjects.ObjectGroupID(
            to_net_guid(object_id), doc
        )
    )


def object_group_ids(object_id, doc) -> list[int]:
    """Get all group IDs for an object."""
    return list(
        _NetObjects.ObjectGroupIDs(
            to_net_guid(object_id), doc
        )
    )
