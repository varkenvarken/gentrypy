from collections import defaultdict


class Tree:
    """
    A basic Tree object has one attribute "children" which is an default dict.

    The keys are names, the values are lists of Tree objects.

    If the children argument is given, it must be a defaultdict or it will be converted to one.
    """
    def __init__(self, children: defaultdict[str, list["Tree"]] | dict[str, list["Tree"]] | None = None):
        self.children: defaultdict[str, list[Tree]] = (
            defaultdict(list) if children is None else defaultdict(list, **children) 
        )


class Visitor:
    def __init__(self, root: Tree, strict: bool = False) -> None:
        self.root = root
        self.strict = strict
        self.result = None

    def visit(self):
        self.result = self._visit(self.root)
        return self.result

    def _get_visitor(self, tree: Tree):
        typename = tree.__class__.__name__
        for klass in self.__class__.__mro__:
            generic_visitor = f"_do_{klass.__name__.lower()}"
            visitor = f"{generic_visitor}_{typename}"
            if hasattr(self, visitor):
                return getattr(self, visitor)
            elif not self.strict and hasattr(self, generic_visitor):
                return getattr(self, generic_visitor)
        raise NotImplementedError(
                f"class {self.__class__.__name__} missing {visitor} and {generic_visitor} methods."
            )

    # children first, then self (bottom-up a.k.a. breadth-first)
    def _visit(self, tree: Tree):
        typename = tree.__class__.__name__
        results: defaultdict[str, list] = defaultdict(list)
        for group, children in tree.children.items():
            for child in children:
                results[group].append(self._visit(child))

        result = self._get_visitor(tree)(tree)
        return {typename: result, "children": results}

import json
class Count(Visitor):
    def _do_count(self, tree:Tree):
        return 1
    
    @staticmethod
    def _sum(d):
        total = 0
        match(d):
            case dict(mapping):
                total += sum(Count._sum(v) for v in d.values())
            case list(iterable):
                total += sum(Count._sum(v) for v in d)
            case int(value):
                total += value
        return total

    def count(self):
        results = self.visit()
        # print(json.dumps(results, indent=4))
        return self._sum(results)