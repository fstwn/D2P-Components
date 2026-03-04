from __future__ import annotations

from D2P.Core.Platforms import GHComponent as _NetGHComponent

from d2p_core._type_utils import _unwrap
from d2p_core._component_base import ComponentBase


class GHComponent(ComponentBase):
    """Python wrapper for D2P.Core.Platforms.GHComponent.

    Use this class to **create new** Grasshopper components.
    For wrapping components returned from utility functions,
    see ``ComponentBase``.

    Properties (TypeId, TypeName, LayerColor, LabelSize, ID,
    GroupIndex, Name, ShortName, Plane, Geometry, Label,
    AllMembers, DynamicMembers, StaticMembers) are delegated
    to the underlying .NET object via __getattr__.
    """

    def __init__(self, component_type, name: str, plane):
        """Create a new GHComponent.

        Args:
            component_type: D2P.Core.Components.ComponentType or wrapper.
            name: Short name for the component.
            plane: Rhino.Geometry.Plane placement.
        """
        net_obj = _NetGHComponent(
            _unwrap(component_type), name, plane
        )
        super().__init__(net_obj)

    @classmethod
    def _wrap(cls, net_obj):
        """Wrap an existing .NET GHComponent instance."""
        if net_obj is None:
            return None
        inst = cls.__new__(cls)
        inst._net_obj = _unwrap(net_obj)
        return inst

    def __repr__(self) -> str:
        return f'GHComponent({self.Name!r}, ID={self.ID})'
