"""Unit tests verifying pure computational correctness of GenericTreeModel."""

from __future__ import annotations

from animora.datastructures.tree import GenericTreeModel


def test_tree_model_insertion_and_traversal() -> None:
    """Verify tree insertion and preorder DFS sequence."""
    tree = GenericTreeModel("root")
    assert tree.traverse_preorder() == ["root"]

    tree.insert_child("root", "child1")
    tree.insert_child("root", "child2")
    tree.insert_child("child1", "grandchild1")

    assert tree.traverse_preorder() == ["root", "child1", "grandchild1", "child2"]
