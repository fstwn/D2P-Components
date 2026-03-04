"""
d2p_core — Python wrapper for D2P.Core .NET library (Rhino 8 / Grasshopper).
"""

from d2p_core._runtime import initialize, is_running_in_rhino, PACKAGE_VERSION

__version__ = PACKAGE_VERSION

initialize()

from d2p_core._component_base import ComponentBase  # NOQA: E402
from d2p_core._gh_component import GHComponent  # NOQA: E402
from d2p_core._member_geo import MemberGeo  # NOQA: E402
from d2p_core._component_type import ComponentType  # NOQA: E402
from d2p_core._component_table import ComponentTable  # NOQA: E402
from d2p_core._filter_options import FilterOptions  # NOQA: E402
from d2p_core._layer_info import LayerInfo, LayerInfoComparer  # NOQA: E402
from d2p_core._settings import Settings  # NOQA: E402
from d2p_core import utility  # NOQA: E402

__all__ = [
    '__version__',
    'ComponentBase',
    'GHComponent',
    'MemberGeo',
    'ComponentType',
    'ComponentTable',
    'FilterOptions',
    'LayerInfo',
    'LayerInfoComparer',
    'Settings',
    'is_running_in_rhino',
    'utility',
]


def __dir__():
    """
    Hide snake_case submodules and only show actual classes.
    """
    return __all__
