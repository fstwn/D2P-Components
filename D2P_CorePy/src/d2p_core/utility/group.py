from __future__ import annotations

from D2P_Core.Utility import Group as _NetGroup

from d2p_core._type_utils import to_net_guid, to_net_guids


def add_group(doc, object_ids=None) -> int:
    """Create a new group, optionally adding objects by their IDs."""
    if object_ids is None:
        return int(_NetGroup.AddGroup(doc))
    if isinstance(object_ids, str) or not hasattr(object_ids, '__iter__'):
        object_ids = [object_ids]
    return int(_NetGroup.AddGroup(to_net_guids(object_ids), doc))


def add_objects_to_group(object_ids, group_index: int, doc) -> int:
    """Add objects to an existing group by their IDs."""
    return int(_NetGroup.AddObjectsToGroup(to_net_guids(object_ids), group_index, doc))  # NOQA: E501


def remove_object_from_all_groups(object_id, doc) -> bool:
    """Remove a single object from all its groups."""
    return bool(_NetGroup.RemoveObjectFromAllGroups(to_net_guid(object_id), doc))  # NOQA: E501


def remove_objects_from_all_groups(object_ids, doc) -> bool:
    """Remove multiple objects from all their groups."""
    return bool(_NetGroup.RemoveObjectsFromAllGroups(to_net_guids(object_ids), doc))  # NOQA: E501


def get_group_index(component_id, doc) -> int:
    """Get the group index for a component ID. Returns -1 if not found."""
    return int(_NetGroup.GetGroupIndex(to_net_guid(component_id), doc))


def get_all_group_indices(doc) -> list[int]:
    """Get all group indices in the document."""
    return list(_NetGroup.GetAllGroupIndices(doc))
