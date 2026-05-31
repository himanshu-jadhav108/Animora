"""Unit tests for ScatterPlot data visualization component."""

from __future__ import annotations

from animora.core.animation import Animation
from animora.dataviz.axes import Axes
from animora.dataviz.scatter_plot import ScatterPlot


def test_scatter_plot_point_count_and_mapping() -> None:
    """Verify ScatterPlot point mapping and dot count."""
    points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (7.0, 8.0)]
    axes = Axes(x_range=(0, 10, 1), y_range=(0, 10, 1))

    mapped = ScatterPlot.map_points(points, axes)
    assert len(mapped) == 4

    plot = ScatterPlot(points=points, axes=axes)
    assert len(plot.dots) == 4

    anim = plot.animate_plot()
    assert isinstance(anim, Animation)
    assert anim.name == "plot_points"
