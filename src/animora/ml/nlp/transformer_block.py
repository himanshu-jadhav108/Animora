"""Minimal single-head Transformer Block combining Attention and Feed-Forward layers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.panel import Panel
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.ml.nlp.attention import AttentionModel
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class TransformerBlockModel:
    """Mathematical composition of Single-Head Self-Attention and a Feed-Forward Network.

    EXCLUSION SPECIFICATION:
    For pedagogical simplicity and visual clarity, the following components from standard
    production Transformer architectures (Vaswani et al., 2017) are deliberately excluded:
    1. Multi-Head Attention: Excluded in favor of single-head attention so intermediate matrix
       multiplications remain 1-to-1 legible.
    2. Positional Encoding: Excluded because token ordering is implicit in the sequence index.
    3. Layer Normalization: Excluded to keep numbers directly traceable to raw matrix sums.
    4. Residual / Skip Connections: Excluded to prevent visual clutter and maintain clean linear
       stage transitions.
    """

    def __init__(
        self,
        inputs: Sequence[Sequence[float]] | np.ndarray,
        *,
        d_k: int = 3,
        d_ff: int = 4,
        random_seed: int = 42,
    ) -> None:
        self.X = np.asarray(inputs, dtype=float)
        self.seq_len, self.embed_dim = self.X.shape
        self.d_k = max(1, int(d_k))
        self.d_ff = max(1, int(d_ff))
        self.trace = MLTrace()

        # 1. Attention sublayer
        self.attention_model = AttentionModel(self.X, d_k=self.d_k, random_seed=random_seed)
        self.attn_output = self.attention_model.output

        # 2. Feed-forward sublayer: Linear -> ReLU -> Linear
        rng = np.random.default_rng(random_seed + 1)
        self.W1 = rng.normal(0.0, 1.0, size=(self.d_k, self.d_ff))
        self.b1 = np.zeros(self.d_ff)
        self.W2 = rng.normal(0.0, 1.0, size=(self.d_ff, self.embed_dim))
        self.b2 = np.zeros(self.embed_dim)

        hidden_ff = np.maximum(0.0, np.dot(self.attn_output, self.W1) + self.b1)
        self.ffn_output = np.dot(hidden_ff, self.W2) + self.b2

        self.trace.record(
            name="transformer_block_forward",
            description=f"Computed transformer block for {self.seq_len} tokens.",
            attn_output=self.attn_output.tolist(),
            ffn_output=self.ffn_output.tolist(),
        )


class TransformerBlockVisualizer(MLComponent):
    """Visualizes token inputs flowing through Attention and Feed-Forward stages."""

    def __init__(
        self,
        inputs: Sequence[Sequence[float]] | np.ndarray,
        *,
        tokens: Sequence[str] | None = None,
        d_k: int = 3,
        d_ff: int = 4,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.inputs = np.asarray(inputs, dtype=float)
        self.tokens = (
            list(tokens) if tokens is not None else [f"tok_{i}" for i in range(len(self.inputs))]
        )
        self.model = TransformerBlockModel(self.inputs, d_k=d_k, d_ff=d_ff)

        # Stage cards
        self.attn_card = Panel(
            Text(f"Q, K, V (d_k={self.model.d_k})\nSoftmax(QK^T / sqrt(d)) V", font_size=12),
            title="1. Self-Attention",
            width=3.2,
            height=1.3,
        )
        self.attn_card.move_to(np.array([-1.8, 0.0, 0.0]))

        self.ffn_card = Panel(
            Text(f"Linear -> ReLU -> Linear\nhidden_dim={self.model.d_ff}", font_size=12),
            title="2. Feed-Forward",
            width=3.2,
            height=1.3,
        )
        self.ffn_card.move_to(np.array([2.2, 0.0, 0.0]))

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup()
        group.add(self.attn_card.manim_object)
        group.add(self.ffn_card.manim_object)

        # Connecting arrow from Attention to FFN
        arrow = manim.Arrow(
            np.array([-0.2, 0.0, 0.0]),
            np.array([0.6, 0.0, 0.0]),
            color=active_theme.colors.accent,
            buff=0.0,
        )
        group.add(arrow)
        return group

    def animate(self) -> list[Animation]:
        """One-call animation visualizing data flow through transformer block stages."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Animate Attention Stage
        animations.append(self.attn_card.animate_create(run_time=0.7))

        # 2. Animate Transition Arrow to Feed-Forward Stage
        arrow = manim.Arrow(
            np.array([-0.2, 0.0, 0.0]),
            np.array([0.6, 0.0, 0.0]),
            color=active_theme.colors.accent,
            buff=0.0,
        )
        stage_group = manim.VGroup(arrow, self.ffn_card.manim_object)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(stage_group),
                run_time=0.8,
                name="propagate_to_ffn",
            )
        )

        return animations


def transformer_block(
    inputs: Sequence[Sequence[float]] | np.ndarray,
    *,
    tokens: Sequence[str] | None = None,
    d_k: int = 3,
    d_ff: int = 4,
) -> list[Animation]:
    """One-call functional API to animate data flow through a minimal transformer block."""
    viz = TransformerBlockVisualizer(inputs, tokens=tokens, d_k=d_k, d_ff=d_ff)
    return viz.animate()


__all__ = [
    "TransformerBlockModel",
    "TransformerBlockVisualizer",
    "transformer_block",
]
