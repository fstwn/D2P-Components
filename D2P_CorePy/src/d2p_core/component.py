from __future__ import annotations

from D2P_Core import Component as _NetComponent

from d2p_core._type_utils import to_net_guid


class Component(_NetComponent):
    """Python-friendly subclass of D2P_Core.Component.

    All PascalCase properties (ID, Name, ShortName, IsInitialized,
    ComponentType, Plane, GeometryCollection, etc.) are inherited
    from the .NET base. The wrapper can be passed directly to any
    .NET method expecting D2P_Core.Component.
    """

    def __init__(self, ComponentType, Name: str, Plane):
        """Create a new Component.

        Args:
            ComponentType: D2P_Core.ComponentType or subclass.
            Name: Short name for the component.
            Plane: Rhino.Geometry.Plane placement.
        """
        super().__init__(ComponentType, Name, Plane)

    @classmethod
    def FromID(cls, ComponentType, Guid) -> Component:
        """Wrap an existing component by its ID."""
        return _NetComponent(ComponentType, to_net_guid(Guid))

    def __repr__(self) -> str:
        return f'Component({self.Name!r}, ID={self.ID})'
