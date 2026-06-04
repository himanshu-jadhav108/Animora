"""Unit tests verifying pure computational correctness of LinkedListModel."""

from __future__ import annotations

from animora.datastructures.linked_list import LinkedListModel


def test_linked_list_operations() -> None:
    """Verify insert_head, insert_tail, delete, and search in LinkedListModel."""
    ll = LinkedListModel([20, 30])
    assert ll.to_list() == [20, 30]

    ll.insert_head(10)
    assert ll.to_list() == [10, 20, 30]

    ll.insert_tail(40)
    assert ll.to_list() == [10, 20, 30, 40]

    assert ll.search(30) == 2
    assert ll.search(999) == -1

    assert ll.delete(20) is True
    assert ll.to_list() == [10, 30, 40]

    assert ll.delete(10) is True
    assert ll.to_list() == [30, 40]

    assert ll.delete(999) is False
