"""Unit tests verifying pure computational correctness of ArrayListModel."""

from __future__ import annotations

from animora.datastructures.array import ArrayListModel


def test_array_model_operations() -> None:
    """Verify swap, insert, delete, and set against reference list behavior."""
    model = ArrayListModel([10, 20, 30, 40])
    assert model.to_list() == [10, 20, 30, 40]

    # Swap
    model.swap(0, 3)
    assert model.to_list() == [40, 20, 30, 10]

    # Insert
    model.insert(2, 99)
    assert model.to_list() == [40, 20, 99, 30, 10]

    # Delete
    val = model.delete(1)
    assert val == 20
    assert model.to_list() == [40, 99, 30, 10]

    # Set
    model[0] = 100
    assert model.to_list() == [100, 99, 30, 10]
