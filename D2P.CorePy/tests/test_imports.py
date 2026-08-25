"""Smoke tests for d2p_core package structure and public API."""

import pathlib


# --- structural tests (no .NET needed) ---

def test_dll_bundled():
    """Verify D2P.Core.dll is present in the package lib directory."""
    root_dir = pathlib.Path(__file__).resolve().parent.parent
    lib_dir = root_dir / 'src' / 'd2p_core' / 'lib'
    dll_path = lib_dir / 'D2P.Core.dll'
    assert dll_path.is_file(), f'DLL not found at {dll_path}'


# --- integration tests (require CLR + RhinoCommon) ---

def test_version_defined():
    """Verify __version__ is set."""
    import d2p_core
    assert hasattr(d2p_core, '__version__')
    assert d2p_core.__version__


def test_public_api_classes():
    """Verify all wrapper classes are importable."""
    from d2p_core import (
        Component,
        GHComponent,
        Member,
        ComponentType,
        ComponentTable,
        FilterOptions,
        LayerInfo,
        LayerInfoComparer,
        Settings,
    )
    for cls in (Component, GHComponent, Member, ComponentType,
                FilterOptions, LayerInfo, LayerInfoComparer):
        assert callable(cls)
    assert hasattr(ComponentTable, 'Keys')
    assert hasattr(Settings, 'RootLayerName')


def test_wrappers_have_netobj_property():
    """Verify wrapper instances expose .NetObj property."""
    from d2p_core import FilterOptions, LayerInfo
    fo = FilterOptions()
    assert hasattr(fo, 'NetObj')
    li = LayerInfo()
    assert hasattr(li, 'NetObj')


def test_utility_submodules():
    """Verify all utility submodules are importable."""
    from d2p_core import utility
    for name in ('components', 'instantiation', 'io',
                 'layers', 'members', 'objects', 'rhdoc'):
        mod = getattr(utility, name, None)
        assert mod is not None, (
            f'utility.{name} not found'
        )
        assert hasattr(mod, '__name__')


def test_settings_is_static():
    """Verify Settings is a static class proxy (cannot be instantiated)."""
    from d2p_core import Settings
    import pytest
    with pytest.raises(TypeError):
        Settings()


def test_settings_exposes_new_api():
    """Settings should expose the angular dimension style and Update()."""
    from d2p_core import Settings
    assert isinstance(Settings.AngularDimensionStyleName, str)
    assert callable(Settings.Update)
