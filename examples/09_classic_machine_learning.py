"""Example 09: Classic Machine Learning in Animora."""

from __future__ import annotations

from animora.core.scene import Scene
from animora.ml.classic.linear_regression import linear_regression
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class ClassicMLScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            x = [1.0, 2.0, 3.0, 4.0]
            y = [2.1, 4.0, 5.9, 8.2]
            self.play(*linear_regression(x, y, steps=5))
