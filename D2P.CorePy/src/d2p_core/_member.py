from __future__ import annotations

from D2P.Core.Components.Member import Member as _NetMember

from d2p_core._type_utils import _unwrap, to_net_color
from d2p_core._component_base import _auto_unwrap

import System.Drawing


class Member:
    """Python wrapper for D2P.Core.Components.Member.Member.

    All .NET properties and methods are delegated via __getattr__.
    Wrapper arguments (objects with .NetObj) are auto-unwrapped
    when calling .NET methods, so ``member.SetObjects(geometries)``
    works without needing ``.NetObj``.

    Use ``.NetObj`` to pass the raw .NET object to Grasshopper
    component outputs or other .NET code outside the wrapper.
    """

    _DIR = [
        'NetObj',
        'Component', 'LayerInfo', 'Attributes', 'Geometry', 'BaseObjects',
        'ParentMember', 'AllMembers', 'DynamicMembers', 'StaticMembers',
        'SetObject', 'SetObjects',
        'SetMember', 'SetMembers', 'FindMember', 'FindMembers',
        'Commit', 'Cache', 'Exists', 'Delete', 'Duplicate',
    ]

    def __init__(
        self,
        component,
        layer_info_or_name,
        layer_color: tuple | System.Drawing.Color | None = None,
    ):
        """Create a Member.

        Can be called as::

            Member(component, layer_info)
            Member(component, 'RawLayerName', (R, G, B))

        Args:
            component: IComponentBase or wrapper.
            layer_info_or_name: ILayerInfo/wrapper, or raw layer name string.
            layer_color: Required when layer_info_or_name is a string.
        """
        c = _unwrap(component)
        if isinstance(layer_info_or_name, str):
            net_obj = _NetMember(
                c, layer_info_or_name,
                to_net_color(layer_color),
            )
        else:
            net_obj = _NetMember(
                c, _unwrap(layer_info_or_name),
            )
        object.__setattr__(self, '_net_obj', net_obj)

    @classmethod
    def _wrap(cls, net_obj):
        """Wrap an existing .NET Member / IMember instance."""
        if net_obj is None:
            return None
        inst = cls.__new__(cls)
        object.__setattr__(inst, '_net_obj', net_obj)
        return inst

    @property
    def NetObj(self):
        """The underlying D2P.Core.Components.Member.Member .NET object."""
        return self._net_obj

    def Commit(self, delete_existing: bool = True) -> None:
        """Write this member's objects to the active document.

        Args:
            delete_existing: Delete objects of the same component that are
                not part of this commit before adding the new ones.
        """
        self._net_obj.Commit(bool(delete_existing))

    def __getattr__(self, name):
        attr = getattr(self._net_obj, name)
        if callable(attr):
            return _auto_unwrap(attr)
        return attr

    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._net_obj, name, _unwrap(value))

    def __dir__(self):
        return self._DIR

    def __repr__(self) -> str:
        li = self.LayerInfo
        return (
            f'Member('
            f'LayerInfo={li.RawLayerName!r})'
        )
