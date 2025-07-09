import pytest
from collections import defaultdict
from tree.tree import Tree, Visitor, Count

def test_tree_init_empty():
    t = Tree()
    assert isinstance(t.children, defaultdict)
    assert len(t.children) == 0

def test_tree_init_with_children_dict():
    child = Tree()
    children = {'a': [child]}
    t = Tree(children)
    assert 'a' in t.children
    assert isinstance(t.children['a'], list)
    assert t.children['a'][0] is child

def test_tree_nested_structure():
    leaf1 = Tree()
    leaf2 = Tree()
    branch = Tree({'b': [leaf1, leaf2]})
    root = Tree({'a': [branch]})
    assert root.children['a'][0] == branch
    assert branch.children['b'] == [leaf1, leaf2]

def test_visitor_traversal_and_result():
    # Minimal Visitor subclass for testing
    class DummyVisitor(Visitor):
        def _do_dummyvisitor_tree(self, tree):
            return "visited"

    t = Tree()
    visitor = DummyVisitor(t)
    result = visitor.visit()
    assert result['Tree'] == "visited"
    assert result['children'] == {}

def test_visitor_strict_mode_raises():
    class DummyVisitor(Visitor):
        pass  # no _do_ method

    t = Tree()
    visitor = DummyVisitor(t, strict=True)
    with pytest.raises(NotImplementedError):
        visitor.visit()

def test_count_single_node():
    t = Tree()
    c = Count(t)
    assert c.count() == 1

def test_count_simple_tree():
    leaf1 = Tree()
    leaf2 = Tree()
    branch = Tree({'b': [leaf1, leaf2]})
    root = Tree({'a': [branch]})
    c = Count(root)
    # root + branch + leaf1 + leaf2 == 4 nodes
    assert c.count() == 4

def test_count_unbalanced_tree():
    leaf1 = Tree()
    branch = Tree({'b': [leaf1]})
    root = Tree({'a': [branch], 'c': []})
    c = Count(root)
    # root + branch + leaf1 == 3 nodes
    assert c.count() == 3

def test_count_empty_children():
    t = Tree()
    t.children['x'] = []
    c = Count(t)
    assert c.count() == 1

def test_sum_helper():
    # test _sum with various nested structures
    d = {'a': [1, 2], 'b': {'c': 3}, 'd': 4}
    assert Count._sum(d) == 10
