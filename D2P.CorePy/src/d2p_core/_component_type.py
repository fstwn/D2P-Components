from __future__ import annotations

from D2P.Core.Components import ComponentType as _NetComponentType

from d2p_core._type_utils import _unwrap, to_net_color
from d2p_core._component_base import _auto_unwrap

import System.Drawing  # NOQA


class ComponentType:
    """Python wrapper for D2P.Core.Components.ComponentType.

    Properties (TypeId, TypeName, LabelSize, LayerColor)
    are delegated to the underlying .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    _DIR = [
        'NetObj',
        'TypeId', 'TypeName', 'LabelSize', 'LayerColor',
    ]

    def __init__(
        self,
        TypeId: str,
        TypeName: str,
        LabelSize: float | None = None,
        LayerColor: tuple | System.Drawing.Color | None = None,
    ):
        lc = (
            None if LayerColor is None
            else to_net_color(LayerColor)
        )
        object.__setattr__(
            self, '_net_obj',
            _NetComponentType(TypeId, TypeName, LabelSize, lc),
        )

    @classmethod
    def FromLayer(cls, layer):
        """Create a ComponentType from a Rhino Layer."""
        inst = cls.__new__(cls)
        object.__setattr__(inst, '_net_obj', _NetComponentType(layer))
        return inst

    @classmethod
    def _wrap(cls, net_obj):
        """Wrap an existing .NET ComponentType instance."""
        inst = cls.__new__(cls)
        object.__setattr__(inst, '_net_obj', net_obj)
        return inst

    @property
    def NetObj(self):
        """The underlying D2P.Core.Components.ComponentType .NET object."""
        return self._net_obj

    def __getattr__(self, name):
        attr = getattr(self._net_obj, name)
        if callable(attr):
            return _auto_unwrap(attr)
        return attr

    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._net_obj, name, _unwrap(value))

    def __dir__(self):
        return self._DIR

    def __repr__(self) -> str:
        return (
            f'ComponentType('
            f'{self.TypeId!r}, {self.TypeName!r})'
        )
