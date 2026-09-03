"""Example 11: NLP and Attention Mechanisms in Animora."""

from __future__ import annotations

from animora.core.scene import Scene
from animora.ml.nlp.tokenization import tokenize
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class NLPAndAttentionScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            self.play(*tokenize("Attention is all you need !"))
