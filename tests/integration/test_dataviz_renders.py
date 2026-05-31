"""Integration test rendering all data visualization components through Manim."""

from __future__ import annotations

import manim
from animora.core.scene import Scene
from animora.dataviz.axes import Axes
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.histogram import Histogram
from animora.dataviz.line_chart import LineChart
from animora.dataviz.scatter_plot import ScatterPlot
from animora.dataviz.table import Table


class DatavizCompositeScene(Scene):
    """Integration scene exercising all 6 dataviz components."""

    def construct(self) -> None:
        # 1. Table
        table = Table(
            data=[["Algorithm", "O(N log N)"], ["Bubble Sort", "O(N^2)"]],
            headers=["Name", "Complexity"],
        )
        self.play(table.animate_create(run_time=0.1))

        # 2. Bar Chart
        bar_chart = BarChart(data=[("A", 20), ("B", 50), ("C", 35)])
        self.play(bar_chart.animate_grow(run_time=0.1))

        # 3. Line Chart & Scatter Plot on shared Axes
        axes = Axes(x_range=(0, 5, 1), y_range=(0, 20, 5))
        line_chart = LineChart(points=[(0, 5), (2, 15), (4, 10)], axes=axes)
        scatter = ScatterPlot(points=[(1, 8), (3, 12)], axes=axes)

        self.play(axes.animate_create(run_time=0.1))
        self.play(line_chart.animate_draw(run_time=0.1))
        self.play(scatter.animate_plot(run_time=0.1))

        # 4. Histogram
        hist = Histogram(data=[1, 2, 2, 3, 3, 3, 4, 5], bins=4)
        self.play(hist.animate_grow(run_time=0.1))


def test_dataviz_scene_render_end_to_end() -> None:
    """Verify composite dataviz scene renders cleanly in Manim dry_run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = DatavizCompositeScene()
        scene.render()
        assert len(scene.mobjects) >= 1
