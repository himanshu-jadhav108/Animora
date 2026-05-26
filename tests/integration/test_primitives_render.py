"""Integration test rendering all visual primitives together in an Animora Scene."""

from __future__ import annotations

import manim
from animora.components.arrow import Arrow
from animora.components.panel import Panel
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.scene import Scene


class PrimitivesCompositeScene(Scene):
    """Integration scene combining Text, Shape, Arrow, and Panel."""

    def construct(self) -> None:
        title = Text("Binary Tree Primitive Demo", font_size=32, color="#38BDF8")
        title.move_to([0, 2.5, 0])

        node_a = Shape.circle(radius=0.4, fill_color="#3B82F6").move_to([-1.5, 0, 0])
        node_b = Shape.circle(radius=0.4, fill_color="#10B981").move_to([1.5, 0, 0])
        edge = Arrow(start=node_a, end=node_b, stroke_color="#38BDF8")

        panel = Panel(node_a, node_b, edge, title="Data Structure Frame", padding=0.4)

        # Play animations
        self.play(title.animate_fade_in(run_time=0.1))
        self.play(panel.animate_create(run_time=0.1))
        self.play(edge.animate_highlight(run_time=0.1))


def test_primitives_scene_render_end_to_end() -> None:
    """Verify combined primitives scene renders cleanly in Manim dry_run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = PrimitivesCompositeScene()
        scene.render()
        assert len(scene.mobjects) >= 1
