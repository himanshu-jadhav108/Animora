"""Unit tests for GridLayout solver."""

from __future__ import annotations

import pytest
from animora.layout.base import LayoutItem
from animora.layout.grid import GridLayout


def test_grid_layout_2x2() -> None:
    """Verify 4 items in a 2x2 grid matrix."""
    items = [
        LayoutItem(id="0", width=1.0, height=1.0),
        LayoutItem(id="1", width=1.0, height=1.0),
        LayoutItem(id="2", width=1.0, height=1.0),
        LayoutItem(id="3", width=1.0, height=1.0),
    ]
    layout = GridLayout(columns=2, col_spacing=0.5, row_spacing=0.5, center_origin=True)
    res = layout.solve(items)

    assert len(res.positions) == 4
    # Row 0: item 0 (top-left), item 1 (top-right)
    # Row 1: item 2 (bottom-left), item 3 (bottom-right)
    assert pytest.approx(res["0"][0], abs=1e-3) == -0.75
    assert pytest.approx(res["0"][1], abs=1e-3) == 0.75
    assert pytest.approx(res["1"][0], abs=1e-3) == 0.75
    assert pytest.approx(res["1"][1], abs=1e-3) == 0.75
    assert pytest.approx(res["2"][0], abs=1e-3) == -0.75
    assert pytest.approx(res["2"][1], abs=1e-3) == -0.75
    assert pytest.approx(res["3"][0], abs=1e-3) == 0.75
    assert pytest.approx(res["3"][1], abs=1e-3) == -0.75


def test_grid_layout_uneven_count() -> None:
    """Verify 5 items with 3 columns (creates 2 rows)."""
    items = [LayoutItem(id=str(i), width=1.0, height=1.0) for i in range(5)]
    layout = GridLayout(columns=3, col_spacing=0.2, row_spacing=0.2)
    res = layout.solve(items)

    assert len(res.positions) == 5
    # Item 4 is in row 1, col 1
    assert "4" in res


def test_grid_layout_empty_and_single() -> None:
    """Verify empty and single item."""
    layout = GridLayout(columns=2)
    assert len(layout.solve([]).positions) == 0
    assert len(layout.solve([LayoutItem(id="a", width=1.0, height=1.0)]).positions) == 1
