"""Example 10: Deep Learning and Backpropagation in Animora."""

from __future__ import annotations

from animora.core.scene import Scene
from animora.ml.deep_learning.neural_network import neural_network_forward
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class DeepLearningScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            self.play(*neural_network_forward([2, 3, 1], [0.5, -0.5]))
