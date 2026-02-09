from __future__ import annotations

from D2P_Core import Settings as _NetSettings

from d2p_core._type_utils import to_net_color


class Settings:
    """Python wrapper for D2P_Core.Settings.

    All PascalCase properties (RootLayerName, TypeDelimiter, etc.)
    are delegated to the underlying .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
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
        self._net_obj = _NetSettings()
        if RootLayerName is not None:
            self._net_obj.RootLayerName = RootLayerName
        if RootLayerColor is not None:
            self._net_obj.RootLayerColor = (
                to_net_color(RootLayerColor)
            )
        if DimensionStyleName is not None:
            self._net_obj.DimensionStyleName = (
                DimensionStyleName
            )
        if TypeDelimiter is not None:
            self._net_obj.TypeDelimiter = TypeDelimiter
        if LayerDelimiter is not None:
            self._net_obj.LayerDelimiter = LayerDelimiter
        if NameDelimiter is not None:
            self._net_obj.NameDelimiter = NameDelimiter
        if LayerDescriptionDelimiter is not None:
            self._net_obj.LayerDescriptionDelimiter = (
                LayerDescriptionDelimiter
            )
        if LayerNameDelimiter is not None:
            self._net_obj.LayerNameDelimiter = (
                LayerNameDelimiter
            )
        if CountDelimiter is not None:
            self._net_obj.CountDelimiter = CountDelimiter
        if JointDelimiter is not None:
            self._net_obj.JointDelimiter = JointDelimiter

    @property
    def NetObj(self):
        """The underlying D2P_Core.Settings .NET object."""
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
            f'Settings('
            f'RootLayerName={self.RootLayerName!r})'
        )
