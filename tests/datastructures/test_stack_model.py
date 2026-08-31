"""Unit tests verifying pure computational correctness of StackModel."""

from __future__ import annotations

import pytest

from animora.datastructures.stack import StackModel


def test_stack_model_lifo_behavior() -> None:
    """Verify StackModel enforces strict LIFO order."""
    stack = StackModel()
    assert stack.is_empty()
    assert stack.size() == 0

    stack.push("A")
    stack.push("B")
    stack.push("C")

    assert not stack.is_empty()
    assert stack.size() == 3
    assert stack.peek() == "C"

    assert stack.pop() == "C"
    assert stack.pop() == "B"
    assert stack.pop() == "A"
    assert stack.is_empty()

    with pytest.raises(IndexError):
        stack.pop()
