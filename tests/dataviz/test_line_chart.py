"""Unit tests for LineChart data visualization component."""

from __future__ import annotations

from animora.core.animation import Animation
from animora.dataviz.line_chart import LineChart


def test_line_chart_segments_and_dots() -> None:
    """Verify LineChart builds correct number of connecting segments and markers."""
    points = [(0.0, 1.0), (1.0, 3.0), (2.0, 2.0), (3.0, 5.0)]
    chart = LineChart(points=points, show_dots=True)

    # 4 points -> 3 line segments, 4 dots
    assert len(chart._lines) == 3
    assert len(chart._dots) == 4

    anim = chart.animate_draw()
    assert isinstance(anim, Animation)
    assert anim.name == "draw_line_chart"
