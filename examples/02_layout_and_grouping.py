"""Example 02: Automatic Layout Solvers (Grid, Horizontal, Circular)."""

from __future__ import annotations

from animora.core import Scene
from animora.components import Text, Shape, Group
from animora.layout import GridLayout, CircularLayout, HorizontalLayout
from animora.theme import ModernDark, use_theme


class LayoutAndGroupingScene(Scene):
    """Demonstrates automatic Group.arrange() using pure layout solvers."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Create a group of 6 circular nodes
            circles = [Shape.circle(radius=0.4, fill_color="#38BDF8") for _ in range(6)]
            node_group = Group(*circles)

            # 2. Arrange in a 2x3 Grid
            node_group.arrange(GridLayout(columns=3, col_spacing=0.4, row_spacing=0.4))
            self.play(node_group.animate_create(run_time=0.8))
            self.wait(0.5)

            # 3. Rearrange in a Circular Layout
            node_group.arrange(CircularLayout(radius=2.2))
            self.play(node_group.animate_transform(node_group, run_time=0.8))
            self.wait(0.5)


if __name__ == "__main__":
    import manim
    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = LayoutAndGroupingScene()
        scene.render()
