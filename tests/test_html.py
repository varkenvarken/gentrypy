import pytest  # noqa: F401 
from gentry.html import HTMLLayout
from gentry.tree import Tree


class DummyNode(Tree, HTMLLayout): ...


def test_html_str_simple():
    node = DummyNode(label="A")
    result = str(node)
    assert "<html>" in result
    assert '<div class="nodename">A</div>' in result


def test_html_str_with_properties():
    node = DummyNode(label="B", properties={"x": 1, "y": 2}, include_properties=True)
    result = str(node)
    assert '<div class="property"><div class="key">x</div><div class="value">1</div></div>' in result
    assert '<div class="property"><div class="key">y</div><div class="value">2</div></div>' in result


def test_html_str_with_children():
    child = DummyNode(label="child")
    node = DummyNode(label="parent", children={"group": [child]})
    result = str(node)
    assert '<div class="parent"><div class="nodename">parent</div></div>' in result
    assert '<div class="groupname">group</div>' in result
    assert '<div class="leaf"><div class="nodename">child</div></div>' in result
