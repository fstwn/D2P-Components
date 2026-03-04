"""Tests for d2p_core.LayerInfo wrapper."""

from d2p_core import LayerInfo
from d2p_core._type_utils import from_net_color


def test_default_construction():
    """Default LayerInfo should have empty name."""
    li = LayerInfo()
    assert li.RawLayerName == ''


def test_custom_construction():
    """Custom name and color should be set."""
    li = LayerInfo('Geometry', (255, 128, 0, 255))
    assert li.RawLayerName == 'Geometry'
    c = from_net_color(li.LayerColor)
    assert c == (255, 128, 0, 255)


def test_rgb_color_construction():
    """RGB tuple (no alpha) should default alpha to 255."""
    li = LayerInfo('Layer1', (10, 20, 30))
    c = from_net_color(li.LayerColor)
    assert (c[0], c[1], c[2]) == (10, 20, 30)
    assert c[3] == 255


def test_netobj_property_is_dotnet_type():
    """.NetObj should be the raw .NET LayerInfo."""
    from D2P.Core.Components import LayerInfo as _NetLI
    li = LayerInfo('Test', (0, 0, 0))
    assert isinstance(li.NetObj, _NetLI)


def test_repr():
    """__repr__ should contain the layer name."""
    li = LayerInfo('Edges')
    r = repr(li)
    assert 'Edges' in r
    assert 'LayerInfo' in r
