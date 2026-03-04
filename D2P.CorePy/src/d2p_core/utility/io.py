from __future__ import annotations

from D2P.Core.Utility import IO as _NetIO

from d2p_core._type_utils import _unwrap


def export_with_headless(
    component, directory: str,
) -> None:
    """Export a single component using a headless Rhino document."""
    _NetIO.ExportWithHeadless(
        _unwrap(component), directory
    )


def export_components_with_headless(
    components, directory: str, file_name: str,
) -> None:
    """Export multiple components to a single .3dm file."""
    _NetIO.ExportWithHeadless(
        [_unwrap(c) for c in components],
        directory, file_name,
    )
