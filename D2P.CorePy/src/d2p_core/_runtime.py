from __future__ import annotations

import hashlib
import os
import sys
import warnings

from importlib.metadata import PackageNotFoundError, version as _dist_version

DISTRIBUTION_NAME = 'd2p-core-py'
ASSEMBLY_NAME = 'D2P.Core'

_LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')
BUNDLED_DLL_PATH = os.path.join(_LIB_DIR, 'D2P.Core.dll')

# Kept in sync with [project].version so running from a source checkout
# (where no distribution metadata exists) still reports a version.
_FALLBACK_VERSION = '0.1.0'

try:
    PACKAGE_VERSION = _dist_version(DISTRIBUTION_NAME)
except PackageNotFoundError:
    PACKAGE_VERSION = _FALLBACK_VERSION

_UNSTAMPED_VERSION = '0.0.0.0'

_initialized = False
_in_rhino = False
_assembly = None
_assembly_source = None

_RHINO_SYSTEM_PATHS = [
    os.environ.get('D2P_RHINO_SYSTEM_PATH', ''),
    r'C:\Program Files\Rhino 8\System',
]

# D2P.Core API this wrapper binds to. A host-provided assembly (the D2P
# Grasshopper plugin) is already loaded and cannot be replaced, so it wins
# over the bundled DLL even when it is older. Probing these turns that
# situation into one clear message instead of a later AttributeError deep
# inside a wrapper call.
_REQUIRED_API = (
    ('D2P.Core.Components.Component', None),
    ('D2P.Core.Components.Member.Member', None),
    ('D2P.Core.Components.Settings', 'Update'),
    ('D2P.Core.Interfaces.IComponentBase', 'Cache'),
    ('D2P.Core.Utility.Objects', 'ObjectsByName'),
)


def is_running_in_rhino() -> bool:
    """True if the current process is a running Rhino instance."""
    return _in_rhino


def assembly_info() -> dict:
    """Describe which D2P.Core assembly is in use.

    Returns a dict with the resolved ``source`` ('host' when Rhino or the
    Grasshopper plugin provided it, 'bundled' when this package loaded its
    own copy), the assembly ``path`` and ``version``, and the bundled DLL
    it was compared against.
    """
    return {
        'source': _assembly_source,
        'path': _assembly_path(_assembly),
        'version': _assembly_version(_assembly),
        'bundled_path': BUNDLED_DLL_PATH,
        'bundled_version': _bundled_version(),
        'in_rhino': _in_rhino,
        'package_version': PACKAGE_VERSION,
    }


def initialize():
    """Initialize the CLR and resolve the D2P.Core assembly.

    When running inside Rhino/Grasshopper, the CLR and RhinoCommon
    are already available. When running outside (e.g. testing), this
    uses the ``rhinoinside`` package to bootstrap a full Rhino
    runtime. It is critical that rhinoinside loads BEFORE any other
    CLR interaction, so we detect Rhino by trying ``import Rhino``
    — not by touching clr or System.
    """
    global _initialized, _in_rhino, _assembly, _assembly_source
    if _initialized:
        return

    try:
        import Rhino  # NOQA: F401
        _in_rhino = True
    except ImportError:
        _in_rhino = False
        _load_rhino_inside()

    import clr

    loaded = _find_loaded_assembly()
    if loaded is not None:
        _assembly = loaded
        _assembly_source = 'host'
        _check_host_assembly(loaded)
    else:
        if not os.path.isfile(BUNDLED_DLL_PATH):
            raise FileNotFoundError(
                f'D2P.Core.dll not found at {BUNDLED_DLL_PATH}'
            )
        if _LIB_DIR not in sys.path:
            sys.path.append(_LIB_DIR)
        clr.AddReference(ASSEMBLY_NAME)
        _assembly = _find_loaded_assembly()
        _assembly_source = 'bundled'

    _initialized = True


def _load_rhino_inside():
    """Use rhinoinside to bootstrap the Rhino runtime."""
    try:
        import rhinoinside
    except ImportError:
        raise RuntimeError(
            'rhinoinside is required to use d2p_core '
            'outside of Rhino.\n'
            'Install it with: pip install d2p-core-py[standalone]'
        )

    rhino_dir = _find_rhino_system_dir()
    if rhino_dir is None:
        raise RuntimeError(
            'Rhino installation not found. Set '
            'D2P_RHINO_SYSTEM_PATH to your Rhino '
            'System directory.'
        )
    rhinoinside.load(rhino_dir, 'net7.0')


def _find_rhino_system_dir() -> str | None:
    for path in _RHINO_SYSTEM_PATHS:
        if path and os.path.isdir(path):
            return path
    return None


def _find_loaded_assembly():
    import System
    for asm in System.AppDomain.CurrentDomain.GetAssemblies():
        if asm.GetName().Name == ASSEMBLY_NAME:
            return asm
    return None


def _check_host_assembly(assembly):
    """Report incompatibilities between a host D2P.Core and the bundled one.

    The host assembly is already loaded, so this only diagnoses — it
    cannot swap in the bundled DLL.
    """
    path = _assembly_path(assembly)
    if path and _file_digest(path) == _file_digest(BUNDLED_DLL_PATH):
        return

    host_version = _assembly_version(assembly)
    bundled_version = _bundled_version()
    versions_comparable = (
        host_version != _UNSTAMPED_VERSION
        and bundled_version not in (None, _UNSTAMPED_VERSION)
    )
    if versions_comparable and host_version != bundled_version:
        warnings.warn(
            f'D2P.Core version mismatch: the already-loaded assembly is '
            f'{host_version}, but d2p_core {PACKAGE_VERSION} bundles '
            f'{bundled_version}. The loaded assembly takes precedence.\n'
            f'Loaded from: {path or "<unknown>"}',
            UserWarning,
            stacklevel=4,
        )

    missing = _missing_api(assembly)
    if not missing:
        return

    message = (
        f'The loaded D2P.Core assembly is missing API that d2p_core '
        f'{PACKAGE_VERSION} requires: {", ".join(missing)}.\n'
        f'Loaded from: {path or "<unknown>"}\n'
        f'Bundled with this package: {BUNDLED_DLL_PATH}\n'
        'This usually means an older D2P Grasshopper plugin is installed. '
        'Its assembly is loaded first and takes precedence over the '
        'bundled one, so update the plugin to match this package.\n'
        'Set D2P_ALLOW_INCOMPATIBLE_DLL=1 to downgrade this to a warning.'
    )
    if os.environ.get('D2P_ALLOW_INCOMPATIBLE_DLL'):
        warnings.warn(message, UserWarning, stacklevel=4)
    else:
        raise RuntimeError(message)


def _missing_api(assembly) -> list[str]:
    missing = []
    for type_name, member_name in _REQUIRED_API:
        net_type = assembly.GetType(type_name)
        if net_type is None:
            missing.append(type_name)
        elif member_name and not len(net_type.GetMember(member_name)):
            missing.append(f'{type_name}.{member_name}')
    return missing


def _assembly_path(assembly) -> str | None:
    if assembly is None:
        return None
    try:
        return str(assembly.Location) or None
    except Exception:
        return None


def _assembly_version(assembly) -> str | None:
    if assembly is None:
        return None
    return _format_version(assembly.GetName().Version)


def _bundled_version() -> str | None:
    if not os.path.isfile(BUNDLED_DLL_PATH):
        return None
    try:
        from System.Reflection import AssemblyName
        name = AssemblyName.GetAssemblyName(BUNDLED_DLL_PATH)
    except Exception:
        return None
    return _format_version(name.Version)


def _format_version(version) -> str:
    return (
        f'{version.Major}.{version.Minor}.'
        f'{version.Build}.{version.Revision}'
    )


def _file_digest(path) -> str | None:
    if not path or not os.path.isfile(path):
        return None
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()
