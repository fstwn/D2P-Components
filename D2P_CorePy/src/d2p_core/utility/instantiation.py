from __future__ import annotations

from D2P_Core.Utility import Instantiation as _NetInstantiation

from d2p_core._type_utils import to_net_guids


def instances_by_name(
    name: str, settings, doc=None,
) -> list:
    """Find component instances matching a name."""
    return list(
        _NetInstantiation.InstancesByName(
            name, settings, doc
        )
    )


def instances_by_name_from_component(
    component, doc=None,
) -> list:
    """Find instances using a component's name and settings."""
    return list(
        _NetInstantiation.InstancesByName(component, doc)
    )


def instances_by_type(
    type_id: str, settings, filter_options, doc=None,
) -> list:
    """Find component instances by type ID with filter."""
    return list(
        _NetInstantiation.InstancesByType(
            type_id, settings, filter_options, doc,
        )
    )


def instances_from_objects(
    objects, settings, doc=None,
) -> list:
    """Create component instances from RhinoObject collection."""
    return list(
        _NetInstantiation.InstancesFromObjects(
            objects, settings, doc
        )
    )


def instances_from_object_ids(
    object_ids, settings, doc=None,
) -> list:
    """Create component instances from object GUIDs."""
    return list(
        _NetInstantiation.InstancesFromObjects(
            to_net_guids(object_ids), settings, doc,
        )
    )


def instance_from_group(
    group_index: int, settings, doc=None,
):
    """Get a single component instance from a group index."""
    return _NetInstantiation.InstanceFromGroup(
        group_index, settings, doc
    )


def instances_from_groups(
    group_indices, settings, doc=None,
) -> list:
    """Get component instances from group indices."""
    return list(filter(None, [
        c
        for c in _NetInstantiation.InstancesFromGroups(
            group_indices, settings, doc
        )
    ]))


def get_parent_component(
    component, doc=None,
) -> tuple:
    """Get the parent component.

    Returns (parent_component, parents_found).
    """
    result, parents_found = (
        _NetInstantiation.GetParentComponent(
            component, doc
        )
    )
    return result, int(parents_found)


def get_children(
    component, filter_types=None, doc=None,
) -> list:
    """Get child components, optionally filtered by type."""
    return list(
        _NetInstantiation.GetChildren(
            component, filter_types, doc
        )
    )


def get_joints(
    component, filter_types=None, doc=None,
) -> list:
    """Get joint components, optionally filtered by type."""
    return list(
        _NetInstantiation.GetJoints(
            component, filter_types, doc
        )
    )


def get_connected_components(
    component, type_filter, doc=None,
) -> list:
    """Get components connected via joints."""
    return list(
        _NetInstantiation.GetConnectedComponents(
            component, type_filter, doc
        )
    )


def get_component_types(settings, doc=None) -> list:
    """Get all component types present in the document."""
    return list(
        _NetInstantiation.GetComponentTypes(settings, doc)
    )
