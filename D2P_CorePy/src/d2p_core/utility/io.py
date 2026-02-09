from __future__ import annotations

from D2P_Core.Utility import IO as _NetIO

from d2p_core._type_utils import _unwrap


def export(component, directory_path: str) -> None:
    """Export a component to a .3dm file via selection."""
    _NetIO.Export(_unwrap(component), directory_path)


def export_with_headless(
    component, directory_path: str,
) -> None:
    """Export a component using a headless Rhino document."""
    _NetIO.ExportWithHeadless(
        _unwrap(component), directory_path
    )


def export_components_with_headless(
    components, directory: str, file_name: str,
) -> None:
    """Export multiple components to a single .3dm file."""
    _NetIO.ExportWithHeadless(
        [_unwrap(c) for c in components],
        directory, file_name,
    )
