"""Example 06: Algorithm Visualization (Quick Sort on Array)."""

from __future__ import annotations

from animora.algorithms import quick_sort
from animora.core import Scene
from animora.datastructures import Array
from animora.theme import ModernDark, use_theme


class QuickSortAlgorithmScene(Scene):
    """Demonstrates Quick Sort algorithm animation driven by real operation trace."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Create Array
            arr = Array([45, 12, 89, 33, 7, 56], cell_width=1.0, cell_height=1.0)
            self.play(arr.animate_create(run_time=0.8))
            self.wait(0.3)

            # 2. Run Quick Sort animations
            sort_anims = quick_sort(arr, run_time=0.3)
            for anim in sort_anims:
                self.play(anim)
            self.wait(0.5)


if __name__ == "__main__":
    import manim

    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = QuickSortAlgorithmScene()
        scene.render()
