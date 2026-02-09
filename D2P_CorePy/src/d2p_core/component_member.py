from __future__ import annotations

from D2P_Core import ComponentMember as _NetComponentMember


class ComponentMember(_NetComponentMember):
    """Python-friendly subclass of D2P_Core.ComponentMember.

    All PascalCase properties (LayerInfo, GeometryBases,
    ObjectAttributes) are inherited from the .NET base.
    """

    def __init__(self, LayerInfo, GeometryBases, Attributes=None):
        """Create a ComponentMember.

        Args:
            LayerInfo: D2P_Core.LayerInfo or subclass.
            GeometryBases: Iterable of GeometryBase.
            Attributes: ObjectAttributes or None.
        """
        super().__init__(LayerInfo, GeometryBases, Attributes)

    def __repr__(self) -> str:
        return (
            f'ComponentMember('
            f'LayerInfo={self.LayerInfo.RawLayerName!r})'
        )
