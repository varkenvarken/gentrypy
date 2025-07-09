import pytest
from tree.tree import Tree

class DummyChild(Tree):
    def _visit_test_DummyChild(self):
        return "visited"

class DummyChildNoVisitor(Tree):
    pass

def make_tree_with_children():
    t = Tree()
    t.children = {
        "group1": [DummyChild(), DummyChild()],
        "group2": [DummyChildNoVisitor()]
    }
    return t

def test_tree_init_empty_children():
    t = Tree()
    assert isinstance(t.children, dict)
    assert t.children == {}

def test_visit_with_visitor_method():
    t = Tree()
    t.children = {
        "group1": [DummyChild()]
    }
    results = t.visit("test")
    assert "group1" in results
    assert results["group1"] == ["visited"]

def test_visit_multiple_children():
    t = Tree()
    t.children = {
        "group1": [DummyChild(), DummyChild()]
    }
    results = t.visit("test")
    assert results["group1"] == ["visited", "visited"]

def test_visit_no_visitor_method_non_strict():
    t = Tree()
    t.children = {
        "group1": [DummyChildNoVisitor()]
    }
    results = t.visit("test")
    assert results["group1"] == []

def test_visit_mixed_children_non_strict():
    t = make_tree_with_children()
    results = t.visit("test")
    assert results["group1"] == ["visited", "visited"]
    assert results["group2"] == []

def test_visit_no_visitor_method_strict_raises():
    t = Tree()
    t.children = {
        "group1": [DummyChildNoVisitor()]
    }
    with pytest.raises(NotImplementedError) as excinfo:
        t.visit("test", strict=True)
    assert "_visit_test_DummyChildNoVisitor" in str(excinfo.value)

def test_visit_mixed_children_strict_raises():
    t = make_tree_with_children()
    with pytest.raises(NotImplementedError):
        t.visit("test", strict=True)
        