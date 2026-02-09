from __future__ import annotations

from D2P_Core import FilterOptions as _NetFilterOptions


class FilterOptions:
    """Python wrapper for D2P_Core.FilterOptions.

    All PascalCase properties (RegexPattern, ReversePattern)
    are delegated to the underlying .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    def __init__(
        self,
        RegexPattern: str = '',
        ReversePattern: bool = False,
    ):
        self._net_obj = _NetFilterOptions()
        self._net_obj.RegexPattern = RegexPattern
        self._net_obj.ReversePattern = ReversePattern

    @property
    def NetObj(self):
        """The underlying D2P_Core.FilterOptions .NET object."""
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
            f'FilterOptions('
            f'RegexPattern={self.RegexPattern!r}, '
            f'ReversePattern={self.ReversePattern})'
        )
