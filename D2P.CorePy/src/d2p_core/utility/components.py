from __future__ import annotations

from D2P.Core.Utility import Components as _NetComponents

from d2p_core._type_utils import _unwrap


def get_parent_component(component) -> tuple:
    """Get the parent component.

    Returns (parent_component, parents_found).
    """
    result, parents_found = (
        _NetComponents.GetParentComponent(_unwrap(component))
    )
    return result, int(parents_found)


def get_child_components(
    component, filter_types=None,
) -> list:
    """Get child components, optionally filtered by type IDs."""
    return list(
        _NetComponents.GetChildComponents(
            _unwrap(component), filter_types,
        )
    )


def get_joint_components(
    component, filter_types=None,
) -> list:
    """Get joint components, optionally filtered by type IDs."""
    return list(
        _NetComponents.GetJointComponents(
            _unwrap(component), filter_types,
        )
    )


def get_connected_components(
    component, type_filter,
) -> list:
    """Get components connected via joints."""
    return list(
        _NetComponents.GetConnectedComponents(
            _unwrap(component), type_filter,
        )
    )


def get_component_types() -> list:
    """Get all component types present in the document."""
    return list(_NetComponents.GetComponentTypes())
