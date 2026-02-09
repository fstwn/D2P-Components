from __future__ import annotations

from D2P_Core import LayerInfo as _NetLayerInfo
from D2P_Core import LayerInfoComparer as _NetLayerInfoComparer

from d2p_core._type_utils import to_net_color


class LayerInfo(_NetLayerInfo):
    """Python-friendly subclass of D2P_Core.LayerInfo.

    All PascalCase properties (RawLayerName, LayerColor) are
    inherited from the .NET base. The constructor accepts a
    Python color tuple for convenience.
    """

    def __init__(
        self,
        RawLayerName: str = '',
        LayerColor: tuple = (0, 0, 0, 255),
    ):
        super().__init__(
            RawLayerName, to_net_color(LayerColor)
        )

    def __repr__(self) -> str:
        return (
            f'LayerInfo({self.RawLayerName!r}, '
            f'LayerColor={self.LayerColor})'
        )


class LayerInfoComparer(_NetLayerInfoComparer):
    """Python-friendly subclass of D2P_Core.LayerInfoComparer."""

    def __init__(self, component):
        super().__init__(component)
