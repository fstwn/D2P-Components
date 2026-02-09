"""
d2p_core — Python wrapper for D2P_Core .NET library (Rhino 8 / Grasshopper).
"""

from d2p_core._runtime import initialize, is_running_in_rhino, PACKAGE_VERSION

__version__ = PACKAGE_VERSION

initialize()

from d2p_core.component import Component  # NOQA:E402
from d2p_core.component_member import ComponentMember  # NOQA:E402
from d2p_core.component_type import ComponentType  # NOQA:E402
from d2p_core.filter_options import FilterOptions  # NOQA:E402
from d2p_core.layer_info import LayerInfo, LayerInfoComparer  # NOQA:E402
from d2p_core.settings import Settings  # NOQA:E402
from d2p_core import utility  # NOQA:E402

__all__ = [
    'Component',
    'ComponentMember',
    'ComponentType',
    'FilterOptions',
    'LayerInfo',
    'LayerInfoComparer',
    'Settings',
    'is_running_in_rhino',
    'utility',
]
