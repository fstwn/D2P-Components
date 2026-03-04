"""Tests for d2p_core runtime initialization."""

import d2p_core
from d2p_core._runtime import (
    PACKAGE_VERSION,
    is_running_in_rhino,
    _find_rhino_system_dir,
)


def test_version_matches_constant():
    """__version__ should match PACKAGE_VERSION."""
    assert d2p_core.__version__ == PACKAGE_VERSION


def test_not_running_in_rhino():
    """Outside Rhino, is_running_in_rhino() should be False."""
    assert is_running_in_rhino() is False


def test_rhino_system_dir_found():
    """Rhino system dir should be discovered on this machine."""
    result = _find_rhino_system_dir()
    assert result is not None


def test_initialize_idempotent():
    """Calling initialize() multiple times should not raise."""
    from d2p_core._runtime import initialize
    initialize()
    initialize()


def test_clr_available_after_init():
    """After init, clr and System should be importable."""
    import clr  # noqa: F401
    import System  # noqa: F401
    assert hasattr(System, 'AppDomain')


def test_d2p_core_assembly_loaded():
    """D2P.Core assembly should be in the loaded assemblies."""
    import System
    names = [
        asm.GetName().Name
        for asm in System.AppDomain.CurrentDomain.GetAssemblies()
    ]
    assert 'D2P.Core' in names


def test_rhinocommon_assembly_loaded():
    """RhinoCommon should be loaded (via rhinoinside)."""
    import System
    names = [
        asm.GetName().Name
        for asm in System.AppDomain.CurrentDomain.GetAssemblies()
    ]
    assert 'RhinoCommon' in names
