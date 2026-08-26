from __future__ import annotations

from D2P.Core.Utility import Objects as _NetObjects
from Rhino.DocObjects import ObjectType as _ObjectType

from d2p_core._type_utils import _unwrap, to_net_guid


def get_component_type_from_object(obj):
    """Get the ComponentType from a RhinoObject."""
    return _NetObjects.GetComponentTypeFromObject(obj)


# --- Objects By Name ---

def objects_by_name(name: str, object_type=None) -> list:
    """Get RhinoObjects in the active document by object name.

    Args:
        name: Name filter, as stored in the object attributes.
        object_type: Rhino.DocObjects.ObjectType to restrict the search to.
            Defaults to any object type.
    """
    if object_type is None:
        object_type = _ObjectType.AnyObject
    return list(_NetObjects.ObjectsByName(name, object_type))


# --- Objects By Layer ---

def objects_by_layer(component, layer_idx: int) -> list:
    """Get RhinoObjects on a layer for a component (by group)."""
    return list(
        _NetObjects.ObjectsByLayer(
            _unwrap(component), layer_idx,
        )
    )


def objects_by_layer_doc(layer) -> list:
    """Get RhinoObjects on a layer from the active document."""
    return list(_NetObjects.ObjectsByLayer(layer))


# --- Geometry By Layer ---

def geometry_by_layer(component, layer_idx: int) -> list:
    """Get GeometryBase objects on a layer for a component."""
    return list(
        _NetObjects.GeometryByLayer(
            _unwrap(component), layer_idx,
        )
    )


# --- Objects By Group ---

def objects_by_group(group_idx: int) -> list:
    """Get RhinoObjects in a group."""
    return list(_NetObjects.ObjectsByGroup(group_idx))


# --- Delete ---

def delete_objects(
    component_or_member, layer=None, recursive: bool = False,
) -> int:
    """Delete objects belonging to a component or member.

    Can be called as::

        delete_objects(component, layer)
        delete_objects(component, layer, recursive=True)
        delete_objects(member)
    """
    unwrapped = _unwrap(component_or_member)
    if layer is not None:
        return int(
            _NetObjects.DeleteObjects(unwrapped, layer, recursive)
        )
    return int(_NetObjects.DeleteObjects(unwrapped))


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


# --- Group IDs ---

def get_object_group_id(object_id) -> int:
    """Get the single group ID for an object."""
    return int(
        _NetObjects.GetObjectGroupID(to_net_guid(object_id))
    )


def get_object_group_ids(object_id) -> list[int]:
    """Get all group IDs for an object."""
    return list(
        _NetObjects.GetObjectGroupIDs(to_net_guid(object_id))
    )
