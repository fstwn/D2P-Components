from __future__ import annotations

from D2P_Core import LayerInfo as _NetLayerInfo
from D2P_Core import LayerInfoComparer as _NetLayerInfoComparer

from d2p_core._type_utils import _unwrap, to_net_color


class LayerInfo:
    """Python wrapper for D2P_Core.LayerInfo.

    All PascalCase properties (RawLayerName, LayerColor)
    are delegated to the underlying .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    def __init__(
        self,
        RawLayerName: str = '',
        LayerColor: tuple = (0, 0, 0, 255),
    ):
        self._net_obj = _NetLayerInfo(
            RawLayerName, to_net_color(LayerColor)
        )

    @property
    def NetObj(self):
        """The underlying D2P_Core.LayerInfo .NET object."""
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
            f'LayerInfo({self.RawLayerName!r}, '
            f'LayerColor={self.LayerColor})'
        )


class LayerInfoComparer:
    """Python wrapper for D2P_Core.LayerInfoComparer."""

    def __init__(self, component):
        self._net_obj = _NetLayerInfoComparer(
            _unwrap(component)
        )

    @property
    def NetObj(self):
        """The underlying D2P_Core.LayerInfoComparer .NET object."""
        return self._net_obj

    def __getattr__(self, name):
        return getattr(self._net_obj, name)
