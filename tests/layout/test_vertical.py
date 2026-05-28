"""Unit tests for VerticalLayout solver."""

from __future__ import annotations

import pytest
from animora.layout.base import LayoutItem
from animora.layout.vertical import VerticalLayout


def test_vertical_layout_even_items() -> None:
    """Verify vertical column layout of 3 items from top to bottom."""
    items = [
        LayoutItem(id="top", width=2.0, height=1.0),
        LayoutItem(id="mid", width=2.0, height=1.0),
        LayoutItem(id="bot", width=2.0, height=1.0),
    ]
    layout = VerticalLayout(spacing=0.5, center_origin=True)
    res = layout.solve(items)

    assert len(res.positions) == 3
    # Total height = 1 + 0.5 + 1 + 0.5 + 1 = 4.0
    assert pytest.approx(res.total_height, abs=1e-3) == 4.0
    assert pytest.approx(res["top"][1], abs=1e-3) == 1.5
    assert pytest.approx(res["mid"][1], abs=1e-3) == 0.0
    assert pytest.approx(res["bot"][1], abs=1e-3) == -1.5


def test_vertical_layout_alignments() -> None:
    """Verify left, right, and center alignments with uneven widths."""
    items = [
        LayoutItem(id="narrow", width=1.0, height=1.0),
        LayoutItem(id="wide", width=3.0, height=1.0),
    ]
    left_layout = VerticalLayout(spacing=0.5, alignment="left")
    left_res = left_layout.solve(items)
    # Left edge of wide is -1.5 -> left edge of narrow is -1.5 -> center is -1.0
    assert pytest.approx(left_res["narrow"][0], abs=1e-3) == -1.0
    assert pytest.approx(left_res["wide"][0], abs=1e-3) == 0.0


def test_vertical_layout_empty_and_single() -> None:
    """Verify edge cases: empty and single item."""
    layout = VerticalLayout()
    empty_res = layout.solve([])
    assert len(empty_res.positions) == 0

    single_res = layout.solve([LayoutItem(id="only", width=1.0, height=2.0)])
    assert len(single_res.positions) == 1
    assert pytest.approx(single_res["only"][1], abs=1e-3) == 0.0
