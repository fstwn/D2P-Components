from __future__ import annotations

from D2P.Core.Components import ComponentTable as _NetComponentTable


class _ComponentTableMeta(type):
    """Metaclass that proxies class-level access to the static
    .NET D2P.Core.Components.ComponentTable class."""

    @property
    def Keys(cls):
        """All registered type ID strings."""
        return list(_NetComponentTable.Keys)

    @property
    def Values(cls):
        """All registered .NET Type objects."""
        return list(_NetComponentTable.Values)


class ComponentTable(metaclass=_ComponentTableMeta):
    """Python proxy for the static D2P.Core.Components.ComponentTable.

    Manages the mapping from component type IDs to .NET types::

        ComponentTable.RegisterComponent[T]('AB')
        ComponentTable.TryGetValue('AB')
        ComponentTable.Keys
    """

    NetClass = _NetComponentTable

    def __init__(self):
        raise TypeError(
            'ComponentTable is a static class and cannot be instantiated.'
        )

    @staticmethod
    def RegisterComponent(type_id: str, net_type):
        """Register a .NET component type by its type ID.

        Note: The C# generic ``RegisterComponent<T>(typeID)`` requires
        passing the .NET Type object directly when called from Python::

            ComponentTable.RegisterComponent('AB', clr.GetClrType(MyComponent))
        """
        _NetComponentTable.RegisterComponent[net_type](type_id)

    @staticmethod
    def TryGetValue(type_id: str):
        """Look up the .NET Type for a type ID.

        Returns the Type or None.
        """
        result, net_type = _NetComponentTable.TryGetValue(type_id)
        return net_type if result else None

    @staticmethod
    def TryGetTypeId(net_type):
        """Look up the type ID for a .NET Type.

        Returns the type ID string or None.
        """
        result, type_id = _NetComponentTable.TryGetTypeId(net_type)
        return str(type_id) if result else None
