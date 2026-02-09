from __future__ import annotations

from D2P_Core import Component as _NetComponent

from d2p_core._type_utils import _unwrap, to_net_guid


class Component:
    """Python wrapper for D2P_Core.Component.

    All PascalCase properties (ID, Name, ShortName, IsInitialized,
    ComponentType, Plane, GeometryCollection, etc.) are delegated
    to the underlying .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    def __init__(self, ComponentType, Name: str, Plane):
        """Create a new Component.

        Args:
            ComponentType: D2P_Core.ComponentType or wrapper.
            Name: Short name for the component.
            Plane: Rhino.Geometry.Plane placement.
        """
        self._net_obj = _NetComponent(
            _unwrap(ComponentType), Name, Plane
        )

    @classmethod
    def FromID(cls, ComponentType, Guid):
        """Wrap an existing component by its ID."""
        inst = cls.__new__(cls)
        inst._net_obj = _NetComponent(
            _unwrap(ComponentType), to_net_guid(Guid)
        )
        return inst

    @property
    def NetObj(self):
        """The underlying D2P_Core.Component .NET object."""
        return self._net_obj

    def __getattr__(self, name):
        return getattr(self._net_obj, name)

    def __setattr__(self, name, value):
        if name == '_net_obj':
            super().__setattr__(name, value)
        else:
            setattr(self._net_obj, name, value)

    def __repr__(self) -> str:
        return f'Component({self.Name!r}, ID={self.ID})'
