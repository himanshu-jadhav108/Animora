"""Unit tests for layout base contracts (LayoutItem, LayoutResult)."""

from __future__ import annotations

from animora.layout.base import LayoutItem, LayoutResult


def test_layout_item_creation() -> None:
    """Verify LayoutItem properties."""
    item = LayoutItem(id="node1", width=2.0, height=1.0, depth=0.5, metadata={"type": "circle"})
    assert item.id == "node1"
    assert item.width == 2.0
    assert item.height == 1.0
    assert item.depth == 0.5
    assert item.metadata["type"] == "circle"


def test_layout_result_access() -> None:
    """Verify LayoutResult lookup, indexing, and containment."""
    res = LayoutResult(
        positions={"a": (1.0, 2.0, 0.0), "b": (3.0, 4.0, 0.0)},
        total_width=4.0,
        total_height=2.0,
    )
    assert res["a"] == (1.0, 2.0, 0.0)
    assert "b" in res
    assert "c" not in res
    assert res.get("c", (0.0, 0.0, 0.0)) == (0.0, 0.0, 0.0)
    assert res.total_width == 4.0
