from __future__ import annotations

from D2P_Core import Settings as _NetSettings

from d2p_core._type_utils import to_net_color


class Settings(_NetSettings):
    """Python-friendly subclass of D2P_Core.Settings.

    All PascalCase properties (RootLayerName, TypeDelimiter, etc.)
    are inherited from the .NET base and work exactly as in D2P_Core.
    The constructor accepts optional overrides for convenience.
    """

    def __init__(
        self,
        RootLayerName: str | None = None,
        RootLayerColor: tuple | None = None,
        DimensionStyleName: str | None = None,
        TypeDelimiter: str | None = None,
        LayerDelimiter: str | None = None,
        NameDelimiter: str | None = None,
        LayerDescriptionDelimiter: str | None = None,
        LayerNameDelimiter: str | None = None,
        CountDelimiter: str | None = None,
        JointDelimiter: str | None = None,
    ):
        super().__init__()
        if RootLayerName is not None:
            self.RootLayerName = RootLayerName
        if RootLayerColor is not None:
            self.RootLayerColor = to_net_color(RootLayerColor)
        if DimensionStyleName is not None:
            self.DimensionStyleName = DimensionStyleName
        if TypeDelimiter is not None:
            self.TypeDelimiter = TypeDelimiter
        if LayerDelimiter is not None:
            self.LayerDelimiter = LayerDelimiter
        if NameDelimiter is not None:
            self.NameDelimiter = NameDelimiter
        if LayerDescriptionDelimiter is not None:
            self.LayerDescriptionDelimiter = (
                LayerDescriptionDelimiter
            )
        if LayerNameDelimiter is not None:
            self.LayerNameDelimiter = LayerNameDelimiter
        if CountDelimiter is not None:
            self.CountDelimiter = CountDelimiter
        if JointDelimiter is not None:
            self.JointDelimiter = JointDelimiter

    def __repr__(self) -> str:
        return (
            f'Settings(RootLayerName={self.RootLayerName!r})'
        )
