"""Integration tests verifying full render of NLP and attention scenes in Manim dry-run mode."""

from __future__ import annotations

import manim

from animora.core.scene import Scene
from animora.ml.nlp import (
    attention,
    tokenize,
    transformer_block,
    word_embeddings,
)
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class TokenizeScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            self.play(*tokenize("Hello world!"))


class WordEmbeddingsScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            self.play(*word_embeddings(["apple", "banana", "cherry"], embed_dim=4))


class AttentionScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            X = [[1.0, 0.5], [0.2, 0.8], [0.4, 0.1]]
            self.play(*attention(X, d_k=2))


class TransformerBlockScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            X = [[1.0, 0.5], [0.2, 0.8]]
            self.play(*transformer_block(X, d_k=2, d_ff=3))


def test_tokenize_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = TokenizeScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_word_embeddings_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = WordEmbeddingsScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_attention_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = AttentionScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_transformer_block_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = TransformerBlockScene()
        scene.render()
        assert len(scene.mobjects) >= 1
