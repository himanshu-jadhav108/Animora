"""Unit tests for FlowLayout solver."""

from __future__ import annotations

import pytest

from animora.layout.base import LayoutItem
from animora.layout.flow import FlowLayout


def test_flow_layout_wrapping() -> None:
    """Verify flow layout wraps onto a second row after wrap_after items."""
    items = [LayoutItem(id=str(i), width=1.0, height=1.0) for i in range(5)]
    layout = FlowLayout(direction="right", spacing=0.5, line_spacing=1.0, wrap_after=3)
    res = layout.solve(items)

    assert len(res.positions) == 5
    # Items 0, 1, 2 should be in row 0 (higher Y)
    # Items 3, 4 should be in row 1 (lower Y)
    assert res["0"][1] > res["3"][1]
    assert pytest.approx(res["0"][1], abs=1e-3) == res["1"][1]
    assert pytest.approx(res["1"][1], abs=1e-3) == res["2"][1]
    assert pytest.approx(res["3"][1], abs=1e-3) == res["4"][1]


def test_flow_layout_empty_and_single() -> None:
    """Verify empty and single item."""
    layout = FlowLayout()
    assert len(layout.solve([]).positions) == 0
    assert len(layout.solve([LayoutItem(id="item", width=1.0, height=1.0)]).positions) == 1
