"""Scaled Dot-Product Attention mechanism model, matrix visualizer, and one-call API."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.ml.tensor_grid import TensorGrid
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class AttentionModel:
    """Computes exact Scaled Dot-Product Attention with verifiable softmax normalization."""

    def __init__(
        self,
        inputs: Sequence[Sequence[float]] | np.ndarray,
        *,
        d_k: int = 3,
        W_q: np.ndarray | None = None,
        W_k: np.ndarray | None = None,
        W_v: np.ndarray | None = None,
        random_seed: int = 42,
    ) -> None:
        self.X = np.asarray(inputs, dtype=float)
        if self.X.ndim != 2:
            raise ValueError("inputs must be a 2D array of shape (seq_len, embed_dim).")

        self.seq_len, self.embed_dim = self.X.shape
        self.d_k = max(1, int(d_k))
        self.trace = MLTrace()

        rng = np.random.default_rng(random_seed)
        self.W_q = (
            np.asarray(W_q, dtype=float)
            if W_q is not None
            else rng.normal(0.0, 1.0, size=(self.embed_dim, self.d_k))
        )
        self.W_k = (
            np.asarray(W_k, dtype=float)
            if W_k is not None
            else rng.normal(0.0, 1.0, size=(self.embed_dim, self.d_k))
        )
        self.W_v = (
            np.asarray(W_v, dtype=float)
            if W_v is not None
            else rng.normal(0.0, 1.0, size=(self.embed_dim, self.d_k))
        )

        # 1. Linear projections
        self.Q = np.dot(self.X, self.W_q)
        self.K = np.dot(self.X, self.W_k)
        self.V = np.dot(self.X, self.W_v)

        # 2. Scaled dot-product scores: (Q @ K.T) / sqrt(d_k)
        self.scale = np.sqrt(self.d_k)
        self.scores = np.dot(self.Q, self.K.T) / self.scale

        # 3. Softmax along last axis (row-wise)
        shifted = self.scores - np.max(self.scores, axis=-1, keepdims=True)
        exp_scores = np.exp(shifted)
        self.attention_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)

        # 4. Output: weights @ V
        self.output = np.dot(self.attention_weights, self.V)

        self.trace.record(
            name="attention_forward",
            description=f"Computed attention for sequence length {self.seq_len}.",
            Q=self.Q.tolist(),
            K=self.K.tolist(),
            V=self.V.tolist(),
            scores=self.scores.tolist(),
            attention_weights=self.attention_weights.tolist(),
            output=self.output.tolist(),
        )


class AttentionVisualizer(MLComponent):
    """Visualizes attention matrices (Q, K, V, Attention Heatmap, Output) via TensorGrids."""

    def __init__(
        self,
        inputs: Sequence[Sequence[float]] | np.ndarray,
        *,
        d_k: int = 3,
        tokens: Sequence[str] | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.model = AttentionModel(inputs, d_k=d_k)
        self.tokens = list(tokens) if tokens is not None else None

        # TensorGrids for the components
        self.weights_grid = TensorGrid(
            self.model.attention_weights, cell_size=0.7, show_labels=True
        )
        self.output_grid = TensorGrid(self.model.output, cell_size=0.7, show_labels=True)

        self.weights_grid.move_to(np.array([-2.2, 0.0, 0.0]))
        self.output_grid.move_to(np.array([2.5, 0.0, 0.0]))

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup()
        group.add(self.weights_grid.manim_object)
        group.add(self.output_grid.manim_object)

        # Titles for grids
        title_w = manim.Text("Attention Weights A", font_size=14, color=active_theme.colors.accent)
        title_w.next_to(self.weights_grid.manim_object, manim.UP, buff=0.25)
        title_o = manim.Text("Output A @ V", font_size=14, color=active_theme.colors.primary)
        title_o.next_to(self.output_grid.manim_object, manim.UP, buff=0.25)

        group.add(title_w, title_o)
        return group

    def animate(self) -> list[Animation]:
        """One-call animation visualizing attention weights and output context matrix."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create attention weight heatmap grid
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(self.weights_grid.manim_object),
                run_time=0.8,
                name="show_attention_weights",
            )
        )

        # 2. Animate transition to output context matrix
        arrow = manim.Arrow(
            np.array([-0.6, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            color=active_theme.colors.secondary,
            buff=0.0,
        )

        out_group = manim.VGroup(arrow, self.output_grid.manim_object)
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(out_group),
                run_time=0.8,
                name="show_attention_output",
            )
        )

        return animations


def attention(
    inputs: Sequence[Sequence[float]] | np.ndarray,
    *,
    d_k: int = 3,
    tokens: Sequence[str] | None = None,
) -> list[Animation]:
    """One-call functional API to animate Scaled Dot-Product Attention."""
    viz = AttentionVisualizer(inputs, d_k=d_k, tokens=tokens)
    return viz.animate()


__all__ = [
    "AttentionModel",
    "AttentionVisualizer",
    "attention",
]
