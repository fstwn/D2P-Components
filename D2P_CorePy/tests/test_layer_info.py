"""Tests for d2p_core.LayerInfo wrapper."""

from d2p_core import LayerInfo

from D2P_Core import LayerInfo as _NetLayerInfo


def test_default_construction():
    """Default LayerInfo should have empty name."""
    li = LayerInfo()
    assert li.RawLayerName == ''


def test_custom_construction():
    """Custom name and color should be set."""
    li = LayerInfo('Geometry', (255, 128, 0, 255))
    assert li.RawLayerName == 'Geometry'
    c = li.LayerColor
    assert (int(c.R), int(c.G), int(c.B), int(c.A)) == (255, 128, 0, 255)


def test_rgb_color_construction():
    """RGB tuple (no alpha) should default alpha to 255."""
    li = LayerInfo('Layer1', (10, 20, 30))
    c = li.LayerColor
    assert (int(c.R), int(c.G), int(c.B)) == (10, 20, 30)
    assert int(c.A) == 255


def test_isinstance_of_net_type():
    """Wrapper instance should be an instance of the .NET base type."""
    li = LayerInfo('Test', (0, 0, 0))
    assert isinstance(li, _NetLayerInfo)


def test_repr():
    """__repr__ should contain the layer name."""
    li = LayerInfo('Edges')
    r = repr(li)
    assert 'Edges' in r
    assert 'LayerInfo' in r
