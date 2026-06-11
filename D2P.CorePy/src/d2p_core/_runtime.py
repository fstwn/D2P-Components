from __future__ import annotations

import os
import sys
import warnings

_LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')
PACKAGE_VERSION = '1.0.2'
_initialized = False
_in_rhino = False

_RHINO_SYSTEM_PATHS = [
    os.environ.get('D2P_RHINO_SYSTEM_PATH', ''),
    r'C:\Program Files\Rhino 8\System',
]


def is_running_in_rhino() -> bool:
    """True if the current process is a running Rhino instance."""
    return _in_rhino


def _find_rhino_system_dir() -> str | None:
    for path in _RHINO_SYSTEM_PATHS:
        if path and os.path.isdir(path):
            return path
    return None


def initialize():
    """Initialize the CLR and load the D2P.Core assembly.

    When running inside Rhino/Grasshopper, the CLR and RhinoCommon
    are already available. When running outside (e.g. testing), this
    uses the ``rhinoinside`` package to bootstrap a full Rhino
    runtime. It is critical that rhinoinside loads BEFORE any other
    CLR interaction, so we detect Rhino by trying ``import Rhino``
    — not by touching clr or System.
    """
    global _initialized, _in_rhino
    if _initialized:
        return

    try:
        import Rhino  # NOQA: F401
        _in_rhino = True
    except ImportError:
        _in_rhino = False
        _load_rhino_inside()

    import clr
    import System

    if _LIB_DIR not in sys.path:
        sys.path.append(_LIB_DIR)

    loaded = None
    for asm in System.AppDomain.CurrentDomain.GetAssemblies():
        if asm.GetName().Name == 'D2P.Core':
            loaded = asm
            break

    if loaded is not None:
        _check_version(loaded)
    else:
        dll_path = os.path.join(_LIB_DIR, 'D2P.Core.dll')
        if not os.path.isfile(dll_path):
            raise FileNotFoundError(
                f'D2P.Core.dll not found at {dll_path}'
            )
        clr.AddReference('D2P.Core')

    _initialized = True


def _load_rhino_inside():
    """Use rhinoinside to bootstrap the Rhino runtime."""
    try:
        import rhinoinside
    except ImportError:
        raise RuntimeError(
            'rhinoinside is required to use d2p_core '
            'outside of Rhino.\n'
            'Install it with: pip install d2p_core[standalone]'
        )

    rhino_dir = _find_rhino_system_dir()
    if rhino_dir is None:
        raise RuntimeError(
            'Rhino installation not found. Set '
            'D2P_RHINO_SYSTEM_PATH to your Rhino '
            'System directory.'
        )
    rhinoinside.load(rhino_dir, 'net7.0')


def _check_version(assembly):
    ver = assembly.GetName().Version
    net_version = f'{ver.Major}.{ver.Minor}.{ver.Build}'
    if net_version != PACKAGE_VERSION:
        warnings.warn(
            f'd2p_core expects D2P.Core.dll {PACKAGE_VERSION}'
            f' but found {net_version}. Consider updating.',
            UserWarning,
            stacklevel=4,
        )
