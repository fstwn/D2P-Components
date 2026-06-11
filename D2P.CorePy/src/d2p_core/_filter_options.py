from __future__ import annotations

from D2P.Core import FilterOptions as _NetFilterOptions

from d2p_core._type_utils import _unwrap
from d2p_core._component_base import _auto_unwrap


class FilterOptions:
    """Python wrapper for D2P.Core.FilterOptions.

    Properties (RegexPattern, ReversePattern) are delegated
    to the underlying .NET object via __getattr__.
    Access the raw .NET object via the .NetObj property.
    """

    _DIR = [
        'NetObj',
        'RegexPattern', 'ReversePattern',
    ]

    def __init__(
        self,
        RegexPattern: str = '',
        ReversePattern: bool = False,
    ):
        object.__setattr__(self, '_net_obj', _NetFilterOptions())
        self._net_obj.RegexPattern = RegexPattern
        self._net_obj.ReversePattern = ReversePattern

    @property
    def NetObj(self):
        """The underlying D2P.Core.FilterOptions .NET object."""
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
            f'FilterOptions('
            f'RegexPattern={self.RegexPattern!r}, '
            f'ReversePattern={self.ReversePattern})'
        )
