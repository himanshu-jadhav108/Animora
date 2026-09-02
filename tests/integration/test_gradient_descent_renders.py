"""Integration test executing full gradient descent animation scene in Manim dry-run mode."""

from __future__ import annotations

import manim

from animora.core.scene import Scene
from animora.ml.optimization.gradient_descent import gradient_descent
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class GradientDescentIntegrationScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):

            def loss(x: float, y: float) -> float:
                return (x**2) + (y**2)

            anims = gradient_descent(loss, start=(2.0, 2.0), steps=5)
            self.play(*anims)


def test_gradient_descent_scene_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = GradientDescentIntegrationScene()
        scene.render()
        assert len(scene.mobjects) >= 1
