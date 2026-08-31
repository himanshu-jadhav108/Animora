"""Unit tests verifying pure computational correctness of QueueModel."""

from __future__ import annotations

import pytest

from animora.datastructures.queue import QueueModel


def test_queue_model_fifo_behavior() -> None:
    """Verify QueueModel enforces strict FIFO order matching collections.deque."""
    queue = QueueModel()
    assert queue.is_empty()

    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    assert queue.peek() == 1
    assert queue.size() == 3

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
    assert queue.is_empty()

    with pytest.raises(IndexError):
        queue.dequeue()
