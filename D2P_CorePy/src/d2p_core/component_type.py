from __future__ import annotations

import d2p_core.settings

from D2P_Core import ComponentType as _NetComponentType

from d2p_core._type_utils import _unwrap, to_net_color

import System.Drawing


class ComponentType:
    """Python wrapper for D2P_Core.ComponentType.

    All PascalCase properties (TypeID, TypeName, LabelSize,
    LayerColor, Settings) are delegated to the underlying
    .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    def __init__(
        self,
        TypeID: str,
        TypeName: str,
        Settings: d2p_core.settings.Settings | None = None,
        LabelSize: float | None = None,
        LayerColor: tuple | System.Drawing.Color | None = None,
    ):
        if not Settings:
            Settings = d2p_core.settings.Settings()
        lc = (
            None if LayerColor is None
            else to_net_color(LayerColor)
        )
        self._net_obj = _NetComponentType(
            TypeID, TypeName, _unwrap(Settings),
            LabelSize, lc,
        )

    @property
    def NetObj(self):
        """The underlying D2P_Core.ComponentType .NET object."""
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
            f'ComponentType('
            f'{self.TypeID!r}, {self.TypeName!r})'
        )
