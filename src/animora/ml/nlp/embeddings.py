"""Word embeddings model, 2D PCA projection visualizer, and one-call animation API."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.ml.base import MLComponent, MLTrace
from animora.ml.classic.pca import PCAModel
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class EmbeddingModel:
    """Mathematical lookup table mapping discrete tokens to illustrative D-dimensional vectors.

    NOTE: This embedding table is purely illustrative (synthetic/random vectors for
    pedagogical visualization) and does not represent pretrained semantic embeddings.
    """

    def __init__(
        self,
        tokens: Sequence[str],
        *,
        embed_dim: int = 4,
        random_seed: int = 42,
    ) -> None:
        self.tokens = list(tokens)
        self.embed_dim = max(2, int(embed_dim))
        self.trace = MLTrace()

        # Generate deterministic synthetic embedding vectors
        rng = np.random.default_rng(random_seed)
        self.embeddings = rng.normal(0.0, 1.0, size=(len(self.tokens), self.embed_dim))

        # Project D-dimensional embeddings down to 2D by directly reusing Phase 13b PCAModel
        self.pca_model: PCAModel | None = None
        if self.embed_dim > 2:
            self.pca_model = PCAModel(self.embeddings, n_components=2)
            # Principal coordinates in 2D space: centered projection onto top 2 components
            self.projected_2d = np.dot(self.pca_model.X_centered, self.pca_model.components[:2].T)
        else:
            self.projected_2d = self.embeddings.copy()

        self.trace.record(
            name="embeddings_computed",
            description=(
                f"Generated {len(self.tokens)} vectors of dimension {self.embed_dim}, "
                f"projected to 2D via PCAModel."
            ),
            tokens=list(self.tokens),
            embed_dim=self.embed_dim,
            projected_2d=self.projected_2d.tolist(),
        )


class EmbeddingVisualizer(MLComponent):
    """Visualizes token embeddings as labeled scatter points on 2D projected axes."""

    def __init__(
        self,
        tokens: Sequence[str],
        *,
        embed_dim: int = 4,
        random_seed: int = 42,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.model = EmbeddingModel(tokens, embed_dim=embed_dim, random_seed=random_seed)

        # Build coordinate axes enclosing the projected points with padding
        x_min = float(np.min(self.model.projected_2d[:, 0]))
        x_max = float(np.max(self.model.projected_2d[:, 0]))
        y_min = float(np.min(self.model.projected_2d[:, 1]))
        y_max = float(np.max(self.model.projected_2d[:, 1]))

        x_span = max(1.0, x_max - x_min)
        y_span = max(1.0, y_max - y_min)
        x_pad = 0.3 * x_span
        y_pad = 0.3 * y_span

        self.axes = Axes(
            x_range=(x_min - x_pad, x_max + x_pad, (x_span + 2 * x_pad) / 4),
            y_range=(y_min - y_pad, y_max + y_pad, (y_span + 2 * y_pad) / 4),
            x_length=6.5,
            y_length=4.5,
        )

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup(self.axes.manim_object)

        for tok, (px, py) in zip(self.model.tokens, self.model.projected_2d, strict=False):
            pt = self.axes.c2p(px, py)
            dot = manim.Dot(pt, radius=0.09, color=active_theme.colors.accent)
            lbl = manim.Text(tok, font_size=13, color=active_theme.colors.text)
            lbl.next_to(dot, manim.UR, buff=0.1)
            group.add(dot, lbl)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation visualizing 2D projected embedding space."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create coordinate space
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(self.axes.manim_object),
                run_time=0.6,
                name="create_embedding_axes",
            )
        )

        # 2. Spawn token points with labels
        dots_group = manim.VGroup()
        for tok, (px, py) in zip(self.model.tokens, self.model.projected_2d, strict=False):
            pt = self.axes.c2p(px, py)
            dot = manim.Dot(pt, radius=0.09, color=active_theme.colors.accent)
            lbl = manim.Text(tok, font_size=13, color=active_theme.colors.text)
            lbl.next_to(dot, manim.UR, buff=0.1)
            dots_group.add(dot, lbl)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(dots_group),
                run_time=0.8,
                name="spawn_projected_tokens",
            )
        )

        return animations


def word_embeddings(
    tokens: Sequence[str],
    *,
    embed_dim: int = 4,
) -> list[Animation]:
    """One-call functional API to animate word embeddings in 2D PCA projected space."""
    viz = EmbeddingVisualizer(tokens, embed_dim=embed_dim)
    return viz.animate()


__all__ = [
    "EmbeddingModel",
    "EmbeddingVisualizer",
    "word_embeddings",
]
