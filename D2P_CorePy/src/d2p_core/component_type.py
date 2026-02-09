from __future__ import annotations

from D2P_Core import ComponentType as _NetComponentType

from d2p_core._type_utils import to_net_color


class ComponentType(_NetComponentType):
    """Python-friendly subclass of D2P_Core.ComponentType.

    All PascalCase properties (TypeID, TypeName, LabelSize,
    LayerColor, Settings) are inherited from the .NET base.
    The constructor accepts a Python color tuple for convenience.
    """

    def __init__(
        self,
        TypeID: str,
        TypeName: str,
        Settings=None,
        LabelSize: float | None = None,
        LayerColor: tuple | None = None,
    ):
        lc = (
            None if LayerColor is None
            else to_net_color(LayerColor)
        )
        super().__init__(
            TypeID, TypeName, Settings, LabelSize, lc
        )

    def __repr__(self) -> str:
        return (
            f'ComponentType('
            f'{self.TypeID!r}, {self.TypeName!r})'
        )
