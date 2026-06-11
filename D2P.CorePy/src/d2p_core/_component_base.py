from __future__ import annotations

import functools

from d2p_core._type_utils import _unwrap


def _auto_unwrap(method):
    """Wrap a .NET method so wrapper arguments are auto-unwrapped."""
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        args = tuple(_unwrap(a) for a in args)
        kwargs = {k: _unwrap(v) for k, v in kwargs.items()}
        return method(*args, **kwargs)
    return wrapper


class ComponentBase:
    """Python wrapper for any D2P.Core IComponentBase instance.

    Use this to wrap component objects returned from utility functions
    (e.g. ``Instantiation.InstanceFromGroup``), which may be the
    internal ``Component`` type rather than ``GHComponent``.

    Can also be subclassed to add Python-side convenience methods::

        class MyBeam(GHComponent):
            def __init__(self, component_type, name, plane):
                super().__init__(component_type, name, plane)
                self._cached_length = None   # use _ prefix for Python attrs

            def get_edges(self):
                return [m for m in self.AllMembers if ...]

    Note: For true component extensibility (static members via
    ``MemberCollection``, registration in ``ComponentTable``),
    the component must be defined in C#. Python subclasses add
    convenience on top of the .NET object but cannot participate
    in the C# instantiation pipeline.

    All .NET properties and methods are delegated via __getattr__.
    Wrapper arguments (objects with .NetObj) are auto-unwrapped
    when calling .NET methods, so ``comp.SetMember(member)`` works
    without needing ``comp.SetMember(member.NetObj)``.

    Use ``.NetObj`` to pass the raw .NET object to Grasshopper
    component outputs or other .NET code outside the wrapper.
    """

    _DIR = [
        'NetObj',
        'TypeId', 'TypeName', 'LayerColor', 'LabelSize',
        'ID', 'GroupIndex', 'Name', 'ShortName', 'Plane',
        'Geometry', 'Label',
        'AllMembers', 'DynamicMembers', 'StaticMembers',
        'SetMember', 'SetMembers', 'FindMember', 'FindMembers',
        'Transform', 'Exists', 'Delete', 'Commit', 'Duplicate',
        'CompareTo',
    ]

    __slots__ = ('_net_obj',)

    def __init__(self, net_obj):
        """Wrap an existing .NET IComponentBase instance.

        Args:
            net_obj: A .NET object implementing IComponentBase.
        """
        object.__setattr__(self, '_net_obj', _unwrap(net_obj))

    @classmethod
    def _wrap(cls, net_obj):
        """Wrap an existing .NET IComponentBase instance."""
        if net_obj is None:
            return None
        inst = cls.__new__(cls)
        object.__setattr__(inst, '_net_obj', _unwrap(net_obj))
        return inst

    @property
    def NetObj(self):
        """The underlying .NET IComponentBase object."""
        return self._net_obj

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
        try:
            return f'ComponentBase({self.Name!r}, ID={self.ID})'
        except Exception:
            return 'ComponentBase(<uninitialized>)'
