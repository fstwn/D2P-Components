from __future__ import annotations

from D2P.Core.Components import Settings as _NetSettings

from d2p_core._type_utils import to_net_color, from_net_color


class _SettingsMeta(type):
    """Metaclass that proxies class-level property access to the
    static .NET D2P.Core.Components.Settings class."""

    # --- Docs ---

    @property
    def ActiveDoc(cls):
        return _NetSettings.ActiveDoc

    @ActiveDoc.setter
    def ActiveDoc(cls, value):
        _NetSettings.ActiveDoc = value

    # --- Layer structure ---

    @property
    def RootLayerName(cls) -> str:
        return str(_NetSettings.RootLayerName)

    @RootLayerName.setter
    def RootLayerName(cls, value: str):
        _NetSettings.RootLayerName = value

    @property
    def RootLayerColor(cls) -> tuple[int, int, int, int]:
        return from_net_color(_NetSettings.RootLayerColor)

    @RootLayerColor.setter
    def RootLayerColor(cls, value):
        _NetSettings.RootLayerColor = to_net_color(value)

    # --- Style ---

    @property
    def DimensionStyleName(cls) -> str:
        return str(_NetSettings.DimensionStyleName)

    @property
    def DimensionStyle(cls):
        return _NetSettings.DimensionStyle

    # --- Tolerance ---

    @property
    def Tolerance(cls) -> float:
        return float(_NetSettings.Tolerance)

    @property
    def AngleTolerance(cls) -> float:
        return float(_NetSettings.AngleTolerance)

    # --- Delimiters ---

    @property
    def TypeDelimiter(cls) -> str:
        return str(_NetSettings.TypeDelimiter)

    @TypeDelimiter.setter
    def TypeDelimiter(cls, value: str):
        _NetSettings.TypeDelimiter = value

    @property
    def LayerDelimiter(cls) -> str:
        return str(_NetSettings.LayerDelimiter)

    @LayerDelimiter.setter
    def LayerDelimiter(cls, value: str):
        _NetSettings.LayerDelimiter = value

    @property
    def NameDelimiter(cls) -> str:
        return str(_NetSettings.NameDelimiter)

    @NameDelimiter.setter
    def NameDelimiter(cls, value: str):
        _NetSettings.NameDelimiter = value

    @property
    def LayerDescriptionDelimiter(cls) -> str:
        return str(_NetSettings.LayerDescriptionDelimiter)

    @LayerDescriptionDelimiter.setter
    def LayerDescriptionDelimiter(cls, value: str):
        _NetSettings.LayerDescriptionDelimiter = value

    @property
    def LayerNameDelimiter(cls) -> str:
        return str(_NetSettings.LayerNameDelimiter)

    @LayerNameDelimiter.setter
    def LayerNameDelimiter(cls, value: str):
        _NetSettings.LayerNameDelimiter = value

    @property
    def CountDelimiter(cls) -> str:
        return str(_NetSettings.CountDelimiter)

    @CountDelimiter.setter
    def CountDelimiter(cls, value: str):
        _NetSettings.CountDelimiter = value

    @property
    def JointDelimiter(cls) -> str:
        return str(_NetSettings.JointDelimiter)

    @JointDelimiter.setter
    def JointDelimiter(cls, value: str):
        _NetSettings.JointDelimiter = value


class Settings(metaclass=_SettingsMeta):
    """Python proxy for the static D2P.Core.Components.Settings class.

    All properties are accessed at the class level (no instantiation needed)::

        Settings.RootLayerName          # read
        Settings.RootLayerName = 'D2P'  # write
        Settings.ActiveDoc             # RhinoDoc
        Settings.TypeDelimiter         # ':'
    """

    NetClass = _NetSettings

    def __init__(self):
        raise TypeError(
            'Settings is a static class and cannot be instantiated. '
            'Access properties directly: Settings.RootLayerName'
        )

    def __repr__(cls):
        return (
            f'Settings('
            f'RootLayerName={cls.RootLayerName!r})'
        )
