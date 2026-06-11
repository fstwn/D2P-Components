from __future__ import annotations

from D2P.Core.Utility import Instantiation as _NetInstantiation

from d2p_core._type_utils import _unwrap, to_net_guids


def instances_by_name(name: str) -> list:
    """Find component instances matching a name."""
    return list(
        _NetInstantiation.InstancesByName(name)
    )


def instances_by_type(
    type_id: str, filter_options,
) -> list:
    """Find component instances by type ID with filter."""
    return list(
        _NetInstantiation.InstancesByType(
            type_id, _unwrap(filter_options),
        )
    )


def instances_from_objects(objects) -> list:
    """Create component instances from RhinoObject collection."""
    return list(
        _NetInstantiation.InstancesFromObjects(objects)
    )


def instances_from_object_ids(object_ids) -> list:
    """Create component instances from object GUIDs."""
    return list(
        _NetInstantiation.InstancesFromObjects(
            to_net_guids(object_ids),
        )
    )


def instance_from_group(group_index: int):
    """Get a single component instance from a group index."""
    return _NetInstantiation.InstanceFromGroup(group_index)


def instance_from_object(obj):
    """Get a component instance from a RhinoObject."""
    return _NetInstantiation.InstanceFromObject(obj)
