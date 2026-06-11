from __future__ import annotations

from D2P.Core.Utility import Members as _NetMembers

from d2p_core._type_utils import _unwrap


def find_members(component) -> list:
    """Find all members for a component from the layer tree."""
    return list(
        _NetMembers.FindMembers(_unwrap(component))
    )


def get_all_member_geometries_from_component(component) -> list:
    """Get all member geometries for a component (flattened)."""
    return list(
        _NetMembers.GetAllMemberGeometries(_unwrap(component))
    )


def get_all_member_geometries(member) -> list:
    """Get all geometries from a member and its children."""
    return list(
        _NetMembers.GetAllMemberGeometries(_unwrap(member))
    )


def member_from_layer(component, layer):
    """Create a member from a component and Rhino Layer."""
    return _NetMembers.MemberFromLayer(
        _unwrap(component), layer,
    )


def is_component_label(component, member) -> bool:
    """Check if a member is the component label."""
    return bool(
        _NetMembers.IsComponentLabel(
            _unwrap(component), _unwrap(member),
        )
    )
