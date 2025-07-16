# gentry
![Python](python.svg) [![Test Status](https://github.com/varkenvarken/blenderaddons-ng/actions/workflows/test_all.yml/badge.svg)](https://github.com/varkenvarken/gentrypy/actions/workflows/test_all.yml) ![Coverage](coverage.svg) ![pypi](pypi.svg)

**gentry** is a Python package for representing and manipulating generic tree structures with support for extensible child groups, visitor patterns, and convenient representations (including Markdown and Mermaid diagrams).

## Features

- **Generic Tree Structure**:  
  The core [`gentry.tree.Tree`](gentry/tree.py) class allows you to define trees with arbitrary child groups, supporting both simple and complex hierarchical data.

- **Customizable Child Groups**:  
  Subclasses can define their own sets of child groups (e.g., `left`, `right`, `children`), enabling flexible tree shapes and semantics.

- **Visitor Pattern**:  
  The [`gentry.tree.Visitor`](gentry/tree.py) class provides a robust visitor pattern implementation, making it easy to traverse and process trees in a structured way.

- **Counting and Analysis**:  
  The [`gentry.tree.Count`](gentry/tree.py) visitor counts nodes in a tree, handling nested and grouped children.

- **Rich Representations**:  
  Trees can be represented as strings, and the package supports exporting to Markdown and Mermaid formats for visualization (see [`gentry.mermaid`](gentry/mermaid.py)).

- **Extensive Testing**:  
  The package includes a comprehensive test suite ([tests/](tests/)) covering initialization, group handling, subclassing, and visitor behaviors.

## Example Usage

```python
from gentry.tree import Tree

class BinaryTree(Tree):
    _groups = {"left", "right"}

root = BinaryTree(label="root")
left = BinaryTree(label="left")
right = BinaryTree(label="right")
root.left.append(left)
root.right.append(right)

print(root)
```

### Using Visitors

```python
from gentry.tree import Visitor

class PrintLabelsVisitor(Visitor):
    def _do_printlabelsvisitor(self, tree):
        print(tree.label)

visitor = PrintLabelsVisitor(root)
visitor.visit()
```

### Counting Nodes

```python
from gentry.tree import Count

counter = Count(root)
print(counter.count())  # Outputs the number of nodes in the tree
```

## Installation

```sh
pip install gentry
```

## License

This project is licensed under the [GNU GPLv3](LICENSE).

## Documentation

- [API Reference](docs/index.html)
- Mermaid/Markdown export: see [`gentry/mermaid.py`](gentry/mermaid.py)

## Project Structure

- [`gentry/tree.py`](gentry/tree.py): Core tree and visitor classes
- [`gentry/mermaid.py`](gentry/mermaid.py): Mermaid/Markdown export utilities
- [`tests/`](tests/): Test suite

---

For more information, see the [project homepage](https://varkenvarken.github.io/gentrypy/)
