"""Unit tests for BarChart data visualization component."""

from __future__ import annotations

import pytest
from animora.dataviz.bar_chart import BarChart


def test_bar_chart_computational_heights() -> None:
    """Verify static computation of bar heights is strictly proportional."""
    values = [20.0, 40.0, 80.0]
    heights = BarChart.compute_bar_heights(values=values, y_max=100.0, y_length=5.0)

    assert len(heights) == 3
    # 20/100 * 5 = 1.0, 40/100 * 5 = 2.0, 80/100 * 5 = 4.0
    assert pytest.approx(heights[0], abs=1e-4) == 1.0
    assert pytest.approx(heights[1], abs=1e-4) == 2.0
    assert pytest.approx(heights[2], abs=1e-4) == 4.0


def test_bar_chart_component_construction() -> None:
    """Verify BarChart constructs correct number of bars matching input data."""
    data = [("A", 10.0), ("B", 25.0), ("C", 15.0)]
    chart = BarChart(data=data)

    assert len(chart.bars) == 3
    assert chart.bars[1].height > chart.bars[0].height
    assert chart.bars[1].height > chart.bars[2].height
