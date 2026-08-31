"""Unit tests verifying pure computational correctness of HeapModel against heapq."""

from __future__ import annotations

import random

from animora.datastructures.heap import HeapModel


def test_heap_model_min_property() -> None:
    """Verify HeapModel extractions strictly produce elements in ascending order."""
    random.seed(42)
    sample_values = [random.randint(1, 100) for _ in range(25)]

    # Animora heap
    heap = HeapModel(sample_values)
    extracted: list[float | int] = []
    while heap.to_list():
        min_val, _ = heap.extract_min()
        extracted.append(min_val)

    # Reference sorted list
    expected = sorted(sample_values)
    assert extracted == expected
