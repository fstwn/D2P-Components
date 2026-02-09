from __future__ import annotations

import System
import System.Drawing as SD


def _unwrap(obj):
    """Extract the .NET object from a wrapper, or pass through."""
    return getattr(obj, 'NetObj', obj)


def to_net_color(value):
    """Convert (R, G, B[, A]) tuple to System.Drawing.Color."""
    if isinstance(value, SD.Color):
        return value
    if isinstance(value, (tuple, list)):
        if len(value) == 4:
            return SD.Color.FromArgb(value[3], value[0], value[1], value[2])
        if len(value) == 3:
            return SD.Color.FromArgb(value[0], value[1], value[2])
    raise ValueError(f'Cannot convert {value!r} to System.Drawing.Color')


def from_net_color(color) -> tuple[int, int, int, int]:
    """Convert System.Drawing.Color to (R, G, B, A) tuple."""
    return (int(color.R), int(color.G), int(color.B), int(color.A))


def to_net_guid(value):
    """Convert string or uuid.UUID to System.Guid, or pass through."""
    if isinstance(value, System.Guid):
        return value
    return System.Guid(str(value))


def from_net_guid(guid) -> str:
    """Convert System.Guid to string."""
    return str(guid)


def to_net_guids(values) -> list:
    """Convert an iterable of guid-like values to a list of System.Guid."""
    return [to_net_guid(v) for v in values]


def to_python_list(enumerable) -> list:
    """Convert .NET IEnumerable to Python list."""
    return list(enumerable)


def to_python_dict(net_dict) -> dict:
    """Convert .NET Dictionary to Python dict."""
    return {kv.Key: kv.Value for kv in net_dict}
