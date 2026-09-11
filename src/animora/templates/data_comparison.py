"""Data Comparison scene template for comparative metrics and benchmarks."""

from __future__ import annotations

from typing import Any

from animora.dataviz.bar_chart import BarChart
from animora.templates.base import BaseTemplateScene
from animora.theme.context import get_active_theme


class DataComparisonTemplate(BaseTemplateScene):
    """Template for comparing performance, benchmarks, or distributions.

    When to use this:
        Use this template when comparing multiple systems, model checkpoints,
        or algorithmic execution profiles side-by-side with metric summary cards
        and visual charts.

    Layout Architecture:
        - Top: Header & Subtitle
        - Center-Left & Center-Right: Comparative visual components / metrics
        - Bottom: Summary insight card
    """

    def __init__(
        self,
        title: str = "Benchmark Comparison",
        subtitle: str = "Latency (ms) Across Frameworks",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.comp_title = title
        self.comp_subtitle = subtitle

    def construct_template(self) -> None:
        active_theme = get_active_theme()

        # 1. Header
        self.setup_header(self.comp_title, self.comp_subtitle)
        self.setup_footer_narrator("Measuring average inference time across 1,000 runs...")

        # 2. Main comparative chart
        chart = BarChart(
            data=[120.0, 45.0, 18.0],
            bar_labels=["Baseline", "Optimized", "Animora Accelerated"],
        )
        chart.move_to([-0.5, -0.2, 0.0])
        self.play(chart.animate_grow(run_time=0.8))

        # 3. Highlight top performer
        self.narrate("Animora Accelerated achieves a 6.6x speedup over Baseline.")
        self.play(chart.animate_highlight(2, color=active_theme.colors.success, run_time=0.6))
        self.wait(0.5)


__all__ = [
    "DataComparisonTemplate",
]
