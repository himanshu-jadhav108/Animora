"""Example 01: Visual Primitives, Text, Shapes, and Animations."""

from __future__ import annotations

from animora.core import Scene
from animora.components import Text, Shape, Panel, Arrow
from animora.theme import ModernDark, use_theme


class BasicsAndShapesScene(Scene):
    """Demonstrates basic Text, Shape, Panel, and Arrow components."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Header Title
            title = Text("Animora Visual Primitives", font_size=38)
            title.move_to([0, 3.0, 0])

            # 2. Geometric Shapes
            circle = Shape.circle(radius=0.6, fill_color="#38BDF8").move_to([-3.0, 0.5, 0])
            rect = Shape.rectangle(width=1.8, height=1.2, fill_color="#818CF8").move_to([0.0, 0.5, 0])
            rounded = Shape.rounded_rectangle(width=1.8, height=1.2, corner_radius=0.2, fill_color="#10B981").move_to([3.0, 0.5, 0])

            # 3. Panel Container
            panel = Panel(circle, rect, rounded, title="Shape Primitives").move_to([0, 0.5, 0])

            # 4. Sequential Animations
            self.play(title.animate_fade_in(run_time=0.5))
            self.play(panel.animate_create(run_time=0.8))
            self.play(circle.animate_highlight(run_time=0.5))
            self.wait(0.5)


if __name__ == "__main__":
    import manim
    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = BasicsAndShapesScene()
        scene.render()
