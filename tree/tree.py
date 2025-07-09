from collections import defaultdict


class Tree:
    def __init__(self):
        self.children: dict[str,list[Tree]] = {}

    def visit(self, function:str, strict:bool=False):
        results:dict[str, list]=defaultdict(list)
        for group, children in self.children.items():
            for child in children:
                typename = child.__class__.__name__
                visitor = f"_visit_{function}_{typename}"
                if hasattr(child, visitor):
                    results[group].append(getattr(child,visitor)())
                elif strict:
                    raise NotImplementedError(visitor)
        return results

