"""Example 08: Mathematical Foundations and Optimization in Animora."""

from __future__ import annotations

from animora.core.scene import Scene
from animora.ml.optimization.gradient_descent import gradient_descent
from animora.ml.surface_plot import SurfacePlot
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class AIMLFoundationsScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):

            def loss(x: float, y: float) -> float:
                return (x**2) + (y**2)

            surface = SurfacePlot(loss, x_range=(-3, 3, 1), y_range=(-3, 3, 1), num_contours=6)
            self.play(surface.animate_create())
            self.play(*gradient_descent(loss, start=(2.0, 2.0), steps=5))
