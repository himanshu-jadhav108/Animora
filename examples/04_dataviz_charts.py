"""Example 04: Data Visualization (BarChart, Table)."""

from __future__ import annotations

from animora.core import Scene
from animora.dataviz import BarChart
from animora.theme import ModernDark, use_theme


class DataVizChartsScene(Scene):
    """Demonstrates BarChart and Table animated components."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Bar Chart
            chart = BarChart(
                data=[("Python", 85), ("Rust", 70), ("Go", 60), ("TypeScript", 75)],
                bar_width=0.7,
            ).move_to([0, 0, 0])

            self.play(chart.animate_grow(run_time=1.0))
            self.play(chart.animate_highlight_bar(0, color="#10B981", run_time=0.5))
            self.wait(0.5)


if __name__ == "__main__":
    import manim

    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = DataVizChartsScene()
        scene.render()
