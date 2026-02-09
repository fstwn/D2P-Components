"""Tests for d2p_core type conversion utilities."""

import uuid

import d2p_core  # noqa: F401 — triggers initialize()
import System
import System.Drawing as SD
from System.Collections.Generic import (
    List as NetList,
    Dictionary as NetDict,
)

from d2p_core._type_utils import (
    _unwrap,
    to_net_color,
    from_net_color,
    to_net_guid,
    from_net_guid,
    to_net_guids,
    to_python_list,
    to_python_dict,
)


# --- _unwrap ---

class _FakeWrapper:
    @property
    def NetObj(self):
        return self._val

    def __init__(self, val):
        self._val = val


def test_unwrap_wrapper():
    """_unwrap extracts .NetObj from wrapper objects."""
    inner = object()
    w = _FakeWrapper(inner)
    assert _unwrap(w) is inner


def test_unwrap_passthrough():
    """_unwrap passes non-wrapper objects through."""
    raw = 'hello'
    assert _unwrap(raw) is raw


# --- color conversions ---

def test_color_rgb_roundtrip():
    """(R, G, B) -> .NET Color -> (R, G, B, A) roundtrip."""
    net = to_net_color((10, 20, 30))
    assert isinstance(net, SD.Color)
    r, g, b, a = from_net_color(net)
    assert (r, g, b) == (10, 20, 30)
    assert a == 255


def test_color_rgba_roundtrip():
    """(R, G, B, A) -> .NET Color -> (R, G, B, A)."""
    net = to_net_color((100, 150, 200, 128))
    result = from_net_color(net)
    assert result == (100, 150, 200, 128)


def test_color_passthrough():
    """Already a .NET Color should pass through."""
    net = SD.Color.FromArgb(1, 2, 3)
    assert to_net_color(net) is net


def test_color_list_input():
    """Lists should work the same as tuples."""
    net = to_net_color([50, 60, 70])
    assert from_net_color(net) == (50, 60, 70, 255)


def test_color_invalid_raises():
    """Invalid input should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        to_net_color('red')
    with pytest.raises(ValueError):
        to_net_color((1,))


# --- GUID conversions ---

def test_guid_string_roundtrip():
    """String GUID -> System.Guid -> string roundtrip."""
    original = '12345678-1234-1234-1234-123456789abc'
    net = to_net_guid(original)
    assert isinstance(net, System.Guid)
    result = from_net_guid(net)
    assert result.lower() == original.lower()


def test_guid_uuid_input():
    """uuid.UUID should be accepted."""
    u = uuid.uuid4()
    net = to_net_guid(u)
    assert from_net_guid(net).lower() == str(u).lower()


def test_guid_passthrough():
    """Already a System.Guid should pass through."""
    net = System.Guid.NewGuid()
    assert to_net_guid(net) is net


def test_guids_batch():
    """to_net_guids converts a list of mixed guid inputs."""
    g1 = '11111111-1111-1111-1111-111111111111'
    g2 = uuid.UUID('22222222-2222-2222-2222-222222222222')
    g3 = System.Guid.NewGuid()
    result = to_net_guids([g1, g2, g3])
    assert len(result) == 3
    assert all(isinstance(g, System.Guid) for g in result)


# --- collection conversions ---

def test_python_list_from_net():
    """to_python_list converts .NET List<T> to Python list."""
    net_list = NetList[System.String]()
    net_list.Add('a')
    net_list.Add('b')
    net_list.Add('c')
    result = to_python_list(net_list)
    assert result == ['a', 'b', 'c']


def test_python_list_empty():
    """Empty .NET list converts to empty Python list."""
    net_list = NetList[System.Int32]()
    assert to_python_list(net_list) == []


def test_python_dict_from_net():
    """to_python_dict converts .NET Dictionary to Python dict."""
    net_dict = NetDict[System.String, System.Int32]()
    net_dict['x'] = 1
    net_dict['y'] = 2
    result = to_python_dict(net_dict)
    assert result == {'x': 1, 'y': 2}


def test_python_dict_empty():
    """Empty .NET dict converts to empty Python dict."""
    net_dict = NetDict[System.String, System.String]()
    assert to_python_dict(net_dict) == {}
