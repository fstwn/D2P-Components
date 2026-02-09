"""Smoke tests for d2p_core package structure and public API."""

import pathlib


# --- structural tests (no .NET needed) ---

def test_dll_bundled():
    """Verify D2P_Core.dll is present in the package lib directory."""
    root_dir = pathlib.Path(__file__).resolve().parent.parent
    lib_dir = root_dir / 'src' / 'd2p_core' / 'lib'
    dll_path = lib_dir / 'D2P_Core.dll'
    assert dll_path.is_file(), f'DLL not found at {dll_path}'


# --- integration tests (require CLR + RhinoCommon) ---

def test_version_defined():
    """Verify __version__ is set and matches the DLL expectation."""
    import d2p_core
    assert hasattr(d2p_core, '__version__')
    assert d2p_core.__version__ == '1.0.1'


def test_public_api_classes():
    """Verify all wrapper classes are importable from the top-level package."""
    from d2p_core import (
        Component,
        ComponentMember,
        ComponentType,
        FilterOptions,
        LayerInfo,
        LayerInfoComparer,
        Settings,
    )
    for cls in (Component, ComponentMember, ComponentType, FilterOptions,
                LayerInfo, LayerInfoComparer, Settings):
        assert callable(cls)


def test_wrappers_inherit_from_net_types():
    """Verify wrappers are subclasses of their .NET counterparts."""
    from D2P_Core import FilterOptions as _NetFilterOptions
    from D2P_Core import LayerInfo as _NetLayerInfo
    from D2P_Core import LayerInfoComparer as _NetLayerInfoComparer
    from D2P_Core import ComponentType as _NetComponentType
    from D2P_Core import ComponentMember as _NetComponentMember
    from D2P_Core import Component as _NetComponent
    from D2P_Core import Settings as _NetSettings

    from d2p_core import (
        Component,
        ComponentMember,
        ComponentType,
        FilterOptions,
        LayerInfo,
        LayerInfoComparer,
        Settings,
    )

    assert issubclass(Settings, _NetSettings)
    assert issubclass(FilterOptions, _NetFilterOptions)
    assert issubclass(LayerInfo, _NetLayerInfo)
    assert issubclass(LayerInfoComparer, _NetLayerInfoComparer)
    assert issubclass(ComponentType, _NetComponentType)
    assert issubclass(ComponentMember, _NetComponentMember)
    assert issubclass(Component, _NetComponent)


def test_utility_submodules():
    """Verify all utility submodules are importable."""
    from d2p_core import utility
    for name in ('group', 'instantiation', 'io', 'layers', 'objects', 'rhdoc'):
        mod = getattr(utility, name, None)
        assert mod is not None, f'utility.{name} not found'
        assert hasattr(mod, '__name__')


def test_layer_scope_enum():
    """Verify the LayerScope enum is defined with expected values."""
    from d2p_core.utility.objects import LayerScope
    assert LayerScope.CURRENT_ONLY.value == 'CurrentOnly'
    assert LayerScope.INCLUDE_CHILDREN.value == 'IncludeChildren'
