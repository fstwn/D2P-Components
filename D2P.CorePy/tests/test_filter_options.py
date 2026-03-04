"""Tests for d2p_core.FilterOptions wrapper."""

from d2p_core import FilterOptions


def test_default_construction():
    """Default FilterOptions should have empty pattern."""
    fo = FilterOptions()
    assert fo.RegexPattern == ''
    assert fo.ReversePattern is False


def test_custom_construction():
    """Custom values should be set in constructor."""
    fo = FilterOptions(
        RegexPattern='^AB', ReversePattern=True
    )
    assert fo.RegexPattern == '^AB'
    assert fo.ReversePattern is True


def test_setter_regex_pattern():
    """Setter should update RegexPattern."""
    fo = FilterOptions()
    fo.RegexPattern = '.*Test.*'
    assert fo.RegexPattern == '.*Test.*'


def test_setter_reverse_pattern():
    """Setter should update ReversePattern."""
    fo = FilterOptions()
    fo.ReversePattern = True
    assert fo.ReversePattern is True


def test_netobj_property_is_dotnet_type():
    """.NetObj should be the raw .NET FilterOptions."""
    from D2P.Core import FilterOptions as _NetFO
    fo = FilterOptions()
    assert isinstance(fo.NetObj, _NetFO)


def test_repr():
    """__repr__ should contain pattern and reverse flag."""
    fo = FilterOptions(
        RegexPattern='test', ReversePattern=True
    )
    r = repr(fo)
    assert 'test' in r
    assert 'True' in r
    assert 'FilterOptions' in r
