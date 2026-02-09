from __future__ import annotations

from D2P_Core.Utility import IO as _NetIO


def export(component, directory_path: str) -> None:
    """Export a component to a .3dm file via selection."""
    _NetIO.Export(component, directory_path)


def export_with_headless(
    component, directory_path: str,
) -> None:
    """Export a component using a headless Rhino document."""
    _NetIO.ExportWithHeadless(component, directory_path)


def export_components_with_headless(
    components, directory: str, file_name: str,
) -> None:
    """Export multiple components to a single .3dm file."""
    _NetIO.ExportWithHeadless(
        list(components), directory, file_name
    )
