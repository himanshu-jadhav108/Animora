"""Unit tests for CircularLayout solver."""

from __future__ import annotations

import pytest

from animora.layout.base import LayoutItem
from animora.layout.circular import CircularLayout


def test_circular_layout_4_items() -> None:
    """Verify 4 items positioned at cardinal angles."""
    items = [LayoutItem(id=str(i), width=0.5, height=0.5) for i in range(4)]
    layout = CircularLayout(radius=2.0, start_angle=0.0, clockwise=False)
    res = layout.solve(items)

    assert len(res.positions) == 4
    # Item 0 at 0 rad -> (2.0, 0.0)
    # Item 1 at pi/2 rad -> (0.0, 2.0)
    # Item 2 at pi rad -> (-2.0, 0.0)
    # Item 3 at 3pi/2 rad -> (0.0, -2.0)
    assert pytest.approx(res["0"][0], abs=1e-3) == 2.0
    assert pytest.approx(res["0"][1], abs=1e-3) == 0.0
    assert pytest.approx(res["1"][0], abs=1e-3) == 0.0
    assert pytest.approx(res["1"][1], abs=1e-3) == 2.0
    assert pytest.approx(res["2"][0], abs=1e-3) == -2.0
    assert pytest.approx(res["2"][1], abs=1e-3) == 0.0


def test_circular_layout_empty_and_single() -> None:
    """Verify empty and single item."""
    layout = CircularLayout(radius=2.0)
    assert len(layout.solve([]).positions) == 0

    single_res = layout.solve([LayoutItem(id="center_node", width=1.0, height=1.0)])
    assert single_res["center_node"] == (0.0, 0.0, 0.0)
