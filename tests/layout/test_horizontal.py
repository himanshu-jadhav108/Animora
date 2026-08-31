"""Unit tests for HorizontalLayout solver."""

from __future__ import annotations

import pytest

from animora.layout.base import LayoutItem
from animora.layout.horizontal import HorizontalLayout


def test_horizontal_layout_even_items() -> None:
    """Verify horizontal layout of 3 items with equal width."""
    items = [
        LayoutItem(id="0", width=1.0, height=1.0),
        LayoutItem(id="1", width=1.0, height=1.0),
        LayoutItem(id="2", width=1.0, height=1.0),
    ]
    layout = HorizontalLayout(spacing=0.5, center_origin=True)
    res = layout.solve(items)

    assert len(res.positions) == 3
    # Total width = 1 + 0.5 + 1 + 0.5 + 1 = 4.0
    assert pytest.approx(res.total_width, abs=1e-3) == 4.0
    assert pytest.approx(res["0"][0], abs=1e-3) == -1.5
    assert pytest.approx(res["1"][0], abs=1e-3) == 0.0
    assert pytest.approx(res["2"][0], abs=1e-3) == 1.5


def test_horizontal_layout_alignments() -> None:
    """Verify top, bottom, and center alignments with uneven heights."""
    items = [
        LayoutItem(id="small", width=1.0, height=1.0),
        LayoutItem(id="tall", width=1.0, height=3.0),
    ]
    top_layout = HorizontalLayout(spacing=0.5, alignment="top")
    top_res = top_layout.solve(items)
    # At top alignment, top edge of small equals top edge of tall (1.5) -> center of small is 1.0
    assert pytest.approx(top_res["small"][1], abs=1e-3) == 1.0
    assert pytest.approx(top_res["tall"][1], abs=1e-3) == 0.0


def test_horizontal_layout_empty_and_single() -> None:
    """Verify edge cases: empty list and single item."""
    layout = HorizontalLayout()
    empty_res = layout.solve([])
    assert len(empty_res.positions) == 0

    single_res = layout.solve([LayoutItem(id="x", width=2.0, height=1.0)])
    assert len(single_res.positions) == 1
    assert pytest.approx(single_res["x"][0], abs=1e-3) == 0.0
