# source: https://object-oriented-python.github.io/9_trees_and_directed_acyclic_graphs.html
from abc import ABC, abstractmethod

plus_one = lambda x: x + 1


def print_output(label, value):
    print(f"{label}: {value}")


# class Transform(ABC):


class TreeNode:
    """A basic tree implementation.

    A tree is simply a collection of connected TreeNodes.

    Parameters
    ----------
    value:
        An arbitrary value associated with this node.
    children:
        The TreeNodes which are the children of this node.
    """

    def __init__(self, *children, **kwargs):
        self.label = kwargs.get("label") or self.default_label
        self.children = list(children)

    def fn(self, input):
        yield plus_one(input)

    def default_label(self):
        # type: () -> str
        return self.__class__.__name__

    # def __repr__(self):
    #     """Return the canonical string representation."""
    #     return f"{type(self).__name__}{(self.label,) + tuple(self.children)}"

    def __str__(self):
        """Serialise the tree recursively as parent -> (children)."""
        childstring = ", ".join(map(str, self.children))
        return f"{self.label!s} -> ({childstring})"  # what does !s mean?

    def __rshift__(self, tree_node):
        self.children = self.children + [tree_node]
        return tree_node

        # self.steps.append(transform.fn)


class Output(TreeNode):
    def fn(self, input):
        print(f"{self.label}: {input}")

class Filter(TreeNode):
    def fn(self, input):
        # print(f"{self.label}: {input}")
        if True:
            yield input


def previsitor(tree, val, fn_parent=None):
    """Traverse tree in preorder applying a function to every node.

    Parameters
    ----------
    tree: TreeNode
        The tree to be visited.
    fn: function(node, fn_parent)
        A function to be applied at each node. The function should take
        the node to be visited as its first argument, and the result of
        visiting its parent as the second.
    """
    fn_out = tree.fn(val)
    if fn_out:
        fn_output = next(fn_out, None)
        if fn_output is not None:
            for child in tree.children:
                previsitor(child, fn_output)

    # print(fn_out)



# def postvisitor(tree, fn):
#     """Traverse tree in postorder applying a function to every node.
#
#     Parameters
#     ----------
#     tree: TreeNode
#         The tree to be visited.
#     fn: function(node, *fn_children)
#         A function to be applied at each node. The function should take the
#         node to be visited as its first argument, and the results of
#         visiting its children as any further arguments.
#     """
#     return fn(tree, *(postvisitor(c, fn) for c in tree.children))


def fn(node, p):
    depth = p + 1 if p else 1
    print(f"{node.value}: {depth}")
    return depth


a = TreeNode(label="a")
b = TreeNode(label="b")
c = TreeNode(label="c")
d = TreeNode(label="d")

e = TreeNode(label="e")
f = TreeNode(label="f")
g = TreeNode(label="g")
h = Filter(label="h")
i = Output(label="i")

# 1.
"""
1.
g >> h >> i

2.
g >> h
g >> i

==
g - i
g - h

3.
g >> h
h >> i
"""

# g >> h >> i  # add i to h

# g >> h >> i
# g >> i

# a -> (b -> (d -> (), e -> (), f -> ()), c -> (g -> ()))

# b >> e
# b >> f
a >> b
b >> d
b >> e
b >> f
a >> c >> g >> h >> i
# b >> d
# a >> c >> g

# tree = TreeNode(
#     "a",
#     TreeNode("b", TreeNode("d"), e, f),
#     TreeNode("c", g)
# )

print(a)

previsitor(a, 2)

# a -> (b -> (d -> (), e -> (), f -> ()), c -> (g -> ()))
# a -> (b -> (d -> (), e -> (), f -> ()), c -> (g -> ()))
# a -> (b -> (d -> (e -> (), f -> ()), c -> (g -> ())))
# a -> (b -> (d -> (e -> (f -> ())), c -> (g -> (h -> (i -> ())))))