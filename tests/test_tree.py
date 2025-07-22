import pytest
from collections import defaultdict
from gentry.tree import Tree


class TestTree:
    def test_init_default_children(self):
        t = Tree(label="root")
        assert t.label == "root"
        assert isinstance(t._children, defaultdict)
        assert t._children == {}

    def test_init_with_children_dict(self):
        child = Tree(label="child")
        children = {"group1": [child]}
        t = Tree(label="root", children=children)
        assert t._children["group1"] == [child]

    def test_init_with_children_defaultdict(self):
        child = Tree(label="child")
        children = defaultdict(list, {"group1": [child]})
        t = Tree(label="root", children=children)
        assert t._children["group1"] == [child]

    def test_getattr_group(self):
        class MyTree(Tree):
            _groups = {"group1"}

        t = MyTree(label="root")
        c = MyTree(label="child")
        t.group1.append(c)
        assert t.group1 == [c]

    def test_getattr_non_group_raises(self):
        t = Tree(label="root")
        with pytest.raises(AttributeError):
            _ = t.nonexistent

    def test_setattr_group(self):
        class MyTree(Tree):
            _groups = {"group1"}

        t = MyTree(label="root")
        c = MyTree(label="child")
        t.group1 = [c]
        assert t._children["group1"] == [c]

    def test_setattr_group_non_list_raises(self):
        class MyTree(Tree):
            _groups = {"group1"}

        t = MyTree(label="root")
        with pytest.raises(AttributeError):
            t.group1 = "notalist"

    def test_setattr_normal(self):
        t = Tree(label="root")
        t.foo = 123
        assert t.foo == 123

    def test_repr(self):
        t = Tree(label="root")
        r = repr(t)
        assert "Tree" in r and "label=root" in r

    def test_groups_inheritance(self):
        class A(Tree):
            _groups = {"left", "right"}

        class B(A):
            pass

        bnode = B(label="b")
        lnode = B(label="left")
        rnode = B(label="right")
        bnode.left.append(lnode)
        bnode.right = [rnode]
        assert bnode.left == [lnode]
        assert bnode.right == [rnode]

    def test_subclass_with_own_groups(self):
        class Base(Tree):
            _groups = {"foo"}

        class Sub(Base):
            _groups = {"bar"}

        s = Sub(label="s")
        b = Sub(label="bar")
        s.bar.append(b)
        assert s.bar == [b]
        # foo should not be a group in Sub
        with pytest.raises(AttributeError):
            _ = s.foo

    def test_subclass_invalid_groups_type(self):
        with pytest.raises(AttributeError):

            class Bad(Tree):
                _groups = ["not", "a", "set"]

    def test_subclass_groups_with_invalid_names(self):
        with pytest.raises(AttributeError):

            class Bad(Tree):
                _groups = {"_bad"}

        with pytest.raises(AttributeError):

            class Bad2(Tree):
                _groups = {"not-valid!"}

        with pytest.raises(AttributeError):

            class Bad3(Tree):
                _groups = {123}

    def test_subclass_groups_are_independent(self):
        class A(Tree):
            _groups = {"left"}

        class B(Tree):
            _groups = {"right"}

        a = A(label="a")
        b = B(label="b")
        lnode = A(label="left")
        rnode = B(label="right")
        a.left.append(lnode)
        b.right.append(rnode)
        assert a.left == [lnode]
        assert b.right == [rnode]
        with pytest.raises(AttributeError):
            _ = a.right
        with pytest.raises(AttributeError):
            _ = b.left
        assert b.right == [rnode]

    def test_is_leaf(self):
        class MyTree(Tree):
            _groups = {"kids"}

        # A node with no children should be a leaf
        t = MyTree(label="root")
        assert t.is_leaf()

        # A node with one child in a group shouldn't be a leaf
        child = MyTree(label="child")
        t.kids.append(child)
        assert not t.is_leaf()

        # A node with multiple children in multiple groups
        t2 = MyTree(label="root2")
        t2.kids.append(MyTree(label="c1"))
        t2.kids.append(MyTree(label="c2"))
        assert not t2.is_leaf()

    def test_initialization_with_keyword_argument(self):
        class A(Tree):
            _groups = {"agroup"}

        child = A(label="child")
        a = A(label="a", agroup=[child])

        assert a.agroup == [child]

    def test_initialization_with_unknown_keyword_argument(self):
        class A(Tree):
            _groups = {"agroup"}

        child = A(label="child")
        with pytest.raises(TypeError):
            _ = A(label="a", unknown=[child])

    def test_initialization_with_duplicated_keyword_argument(self):
        class A(Tree):
            _groups = {"agroup"}

        child = A(label="child")
        with pytest.raises(ValueError):
            _ = A(label="a", agroup=[child], children={"agroup":[child]})

    def test_initialization_with_mixed_group_argument(self):
        class A(Tree):
            _groups = {"agroup", "another_group"}

        child1 = A(label="child1")
        child2 = A(label="child2")

        a = A(label="a", agroup=[child1], children={"another_group":[child2]})
        assert a.agroup == [child1]
        assert a.another_group == [child2]

    def test_subclass_with_implicit_groups(self, capsys):
        class A(Tree):
            def __init__(self, label: str, group1:list[Tree]=[], group2:list[Tree]=[]):
                super().__init__(label, children={"group1":group1,"group2":group2})

        # verify that the init definition style is working
        a1 = A("a1")
        a2 = A("a2")
        a3 = A("a3", group1=[a1], group2=[a2])

        assert a3.group1 == [a1]
        assert a3.group2 == [a2]
        with pytest.raises(AttributeError):
            b = a3.group3  # noqa

        # after instantiation with adding children directly, accessing known groups should still work
        a4 = A("a4")
        a4.group1.append(a1)
        a4.group2.append(a2)

        assert a4.group1 == [a1]
        assert a4.group2 == [a2]
        with pytest.raises(AttributeError):
            b = a4.group3  # noqa
