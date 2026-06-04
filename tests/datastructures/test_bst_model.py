"""Unit tests verifying BST model correctness for insertion, search, and all 3 deletion cases."""

from __future__ import annotations

from animora.datastructures.bst import BSTModel


def test_bst_insertion_and_search_traces() -> None:
    """Verify BST insertion comparisons and search paths."""
    bst = BSTModel()
    # Insert 50 -> root
    trace = bst.insert(50)
    assert trace == []

    # Insert 30 -> visits [50]
    trace = bst.insert(30)
    assert trace == [50]

    # Insert 70 -> visits [50]
    trace = bst.insert(70)
    assert trace == [50]

    # Insert 20 -> visits [50, 30]
    trace = bst.insert(20)
    assert trace == [50, 30]

    # In-order sorted verification
    assert bst.in_order_traversal() == [20, 30, 50, 70]

    # Search existing
    found, s_trace = bst.search(20)
    assert found is True
    assert s_trace == [50, 30, 20]

    # Search non-existing
    found, s_trace = bst.search(40)
    assert found is False
    assert s_trace == [50, 30]


def test_bst_deletion_case_1_leaf() -> None:
    """Verify Case 1: Deletion of a leaf node."""
    bst = BSTModel([50, 30, 70, 20])
    deleted, case_name, _ = bst.delete(20)

    assert deleted is True
    assert case_name == "leaf"
    assert bst.in_order_traversal() == [30, 50, 70]


def test_bst_deletion_case_2_one_child() -> None:
    """Verify Case 2: Deletion of a node with exactly one child."""
    bst = BSTModel([50, 30, 70, 20])  # 30 has only left child 20
    deleted, case_name, _ = bst.delete(30)

    assert deleted is True
    assert case_name == "one_child"
    assert bst.in_order_traversal() == [20, 50, 70]


def test_bst_deletion_case_3_two_children() -> None:
    """Verify Case 3: Deletion of a node with two children (in-order successor replacement)."""
    bst = BSTModel([50, 30, 70, 20, 40, 60, 80])  # 50 has two children: 30 and 70
    deleted, case_name, _ = bst.delete(50)

    assert deleted is True
    assert case_name == "two_children"
    # Successor of 50 is 60, which replaces root
    assert bst.root.value == 60  # type: ignore[union-attr]
    assert bst.in_order_traversal() == [20, 30, 40, 60, 70, 80]
