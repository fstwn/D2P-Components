from __future__ import annotations

from D2P.Core.Components import Component as _NetComponent

from d2p_core._type_utils import _unwrap
from d2p_core._component_base import ComponentBase


class Component(ComponentBase):
    """Python wrapper for D2P.Core.Components.Component.

    The generic fallback component type, used when a document component
    has no dedicated type registered in ``ComponentTable``. Create
    Grasshopper-bound components with ``GHComponent`` instead.

    Properties are delegated to the underlying .NET object via
    __getattr__, as with ``ComponentBase``.
    """

    def __init__(self, name: str | None = None, plane=None):
        """Create a new Component.

        Args:
            name: Short name for the component. Omit for an empty component.
            plane: Rhino.Geometry.Plane placement. Required with ``name``.
        """
        if name is None and plane is None:
            net_obj = _NetComponent()
        elif name is None or plane is None:
            raise TypeError(
                'Component() takes either no arguments or both name and plane'
            )
        else:
            net_obj = _NetComponent(name, plane)
        super().__init__(net_obj)

    @classmethod
    def _wrap(cls, net_obj):
        """Wrap an existing .NET Component instance."""
        if net_obj is None:
            return None
        inst = cls.__new__(cls)
        inst._net_obj = _unwrap(net_obj)
        return inst

    def __repr__(self) -> str:
        return f'Component({self.Name!r}, ID={self.ID})'
