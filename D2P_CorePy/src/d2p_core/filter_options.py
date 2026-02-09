from __future__ import annotations

from D2P_Core import FilterOptions as _NetFilterOptions


class FilterOptions(_NetFilterOptions):
    """Python-friendly subclass of D2P_Core.FilterOptions.

    All PascalCase properties (RegexPattern, ReversePattern) are
    inherited from the .NET base.
    """

    def __init__(
        self,
        RegexPattern: str = '',
        ReversePattern: bool = False,
    ):
        super().__init__()
        self.RegexPattern = RegexPattern
        self.ReversePattern = ReversePattern

    def __repr__(self) -> str:
        return (
            f'FilterOptions('
            f'RegexPattern={self.RegexPattern!r}, '
            f'ReversePattern={self.ReversePattern})'
        )
