"""Algorithm Explainer scene template for step-by-step educational animations."""

from __future__ import annotations

from typing import Any

from animora.components.panel import Panel
from animora.components.text import Text
from animora.datastructures.array import Array
from animora.templates.base import BaseTemplateScene
from animora.theme.context import get_active_theme


class AlgorithmExplainerTemplate(BaseTemplateScene):
    """Template for step-by-step algorithm walkthroughs.

    When to use this:
        Use this template when explaining sequential algorithms (e.g. Bubble Sort,
        Binary Search, Quick Sort, Insertion Sort) where an input data structure
        undergoes discrete comparison, swap, or highlight operations alongside
        synchronized educational commentary.

    Layout Architecture:
        - Top: Title & Algorithm Complexity Badge
        - Center: Primary visualization component (e.g. Array, Graph, or Grid)
        - Bottom: Dynamic narrative explanation bar
    """

    def __init__(
        self,
        title: str = "Algorithm Walkthrough",
        complexity: str = "Time: O(N) | Space: O(1)",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.algo_title = title
        self.complexity_text = complexity
        self.complexity_panel: Panel | None = None

    def construct_template(self) -> None:
        """Default presentation sequence displaying header, badge, array, and narration."""
        active_theme = get_active_theme()

        # 1. Header & Complexity Badge
        self.setup_header(self.algo_title)

        badge_txt = Text(
            self.complexity_text,
            font_size=active_theme.typography.font_size_xs,
            color=active_theme.colors.accent,
        )
        self.complexity_panel = Panel(
            content=badge_txt,
            width=3.6,
            height=0.6,
            fill_color=active_theme.colors.surface,
            stroke_color=active_theme.colors.accent,
        )
        self.complexity_panel.move_to([4.5, 3.2, 0.0])
        self.play(self.complexity_panel.animate_create(run_time=0.4))

        # 2. Narration footer
        self.setup_footer_narrator("Initializing input array...")

        # 3. Primary stage data structure
        arr = Array([38, 27, 43, 3, 9, 82, 10])
        arr.move_to([0.0, 0.2, 0.0])
        self.play(arr.animate_create(run_time=0.8))

        # 4. Exemplar operations
        self.narrate("Comparing index 0 (38) and index 3 (3)...")
        self.play(arr.animate_highlight(0), arr.animate_highlight(3), run_time=0.5)

        self.narrate("Swapping smaller element (3) into earlier position...")
        self.play(arr.animate_swap(0, 3, run_time=0.6))

        self.narrate("Pass complete. Array partially sorted.")
        self.wait(0.5)


__all__ = [
    "AlgorithmExplainerTemplate",
]
