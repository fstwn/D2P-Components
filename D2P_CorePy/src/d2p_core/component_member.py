from __future__ import annotations

from D2P_Core import ComponentMember as _NetComponentMember

from d2p_core._type_utils import _unwrap


class ComponentMember:
    """Python wrapper for D2P_Core.ComponentMember.

    All PascalCase properties (LayerInfo, GeometryBases,
    ObjectAttributes) are delegated to the underlying
    .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    def __init__(self, LayerInfo, GeometryBases, Attributes=None):
        """Create a ComponentMember.

        Args:
            LayerInfo: D2P_Core.LayerInfo or wrapper.
            GeometryBases: Iterable of GeometryBase.
            Attributes: ObjectAttributes or None.
        """
        self._net_obj = _NetComponentMember(
            _unwrap(LayerInfo), GeometryBases, Attributes
        )

    @property
    def NetObj(self):
        """The underlying D2P_Core.ComponentMember .NET object."""
        return self._net_obj

    def __getattr__(self, name):
        return getattr(self._net_obj, name)

    def __setattr__(self, name, value):
        if name == '_net_obj':
            super().__setattr__(name, value)
        else:
            setattr(self._net_obj, name, value)

    def __repr__(self) -> str:
        return (
            f'ComponentMember('
            f'LayerInfo={self.LayerInfo.RawLayerName!r})'
        )
