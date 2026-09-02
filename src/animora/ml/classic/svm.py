"""Hard-margin Support Vector Machine (SVM) model, visualizer, and one-call animation API."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.ml.base import MLComponent, MLTrace
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class HardMarginSVMModel:
    """Mathematical linear SVM solver for linearly-separable 2D datasets."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        y: Sequence[int | float] | np.ndarray,
        *,
        learning_rate: float = 0.01,
        max_iters: int = 500,
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        raw_y = np.asarray(y, dtype=float)
        # Ensure labels are {-1, +1}
        self.y = np.where(raw_y <= 0, -1.0, 1.0)
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.trace = MLTrace()

        self.w = np.zeros(2, dtype=float)
        self.b = 0.0
        self.support_vector_indices: list[int] = []

    def fit(self) -> tuple[np.ndarray, float, list[int]]:
        """Compute optimal separating hyperplane w*x + b = 0 using subgradient descent."""
        self.trace = MLTrace()

        # Subgradient optimization with penalty
        w = np.zeros(2, dtype=float)
        b = 0.0
        C = 50.0  # High penalty for hard margin

        for step in range(self.max_iters):
            margins = self.y * (np.dot(self.X, w) + b)
            violated = margins < 1.0

            grad_w = w - C * np.sum((self.y[violated, np.newaxis] * self.X[violated]), axis=0)
            grad_b = -C * np.sum(self.y[violated])

            lr = self.learning_rate / (1.0 + 0.005 * step)
            w -= lr * grad_w
            b -= lr * grad_b

        self.w = w
        self.b = float(b)

        # Identify support vectors: points closest to margin boundary y*(w*x + b) = 1
        margins = self.y * (np.dot(self.X, self.w) + self.b)
        # Find points within tolerance of minimum margin
        min_margin = np.min(margins)
        sv_indices = np.where(margins <= min_margin + 0.35)[0].tolist()
        self.support_vector_indices = sv_indices

        self.trace.record(
            name="solution",
            description=f"SVM fit: w=[{self.w[0]:.3f}, {self.w[1]:.3f}], b={self.b:.3f}",
            w=tuple(self.w),
            b=self.b,
            support_vectors=self.support_vector_indices,
        )

        return self.w, self.b, self.support_vector_indices


class SVMVisualizer(MLComponent):
    """Component visualizing linear SVM separating hyperplane, margins, and support vectors."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        y: Sequence[int | float] | np.ndarray,
        *,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.model = HardMarginSVMModel(self.X, self.y)
        self.w, self.b, self.sv_indices = self.model.fit()

        x_min, x_max = float(np.min(self.X[:, 0])), float(np.max(self.X[:, 0]))
        y_min, y_max = float(np.min(self.X[:, 1])), float(np.max(self.X[:, 1]))
        x_pad = max(1.0, 0.25 * (x_max - x_min))
        y_pad = max(1.0, 0.25 * (y_max - y_min))

        self.axes = Axes(
            x_range=(x_min - x_pad, x_max + x_pad, (x_max - x_min + 2 * x_pad) / 5),
            y_range=(y_min - y_pad, y_max + y_pad, (y_max - y_min + 2 * y_pad) / 5),
            x_length=7.0,
            y_length=5.0,
        )

        super().__init__(config=config, **kwargs)

    def _get_line_endpoints(self, offset: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        """Compute line endpoints for w*x + b = offset."""
        x_start, x_end = self.axes.x_range[0], self.axes.x_range[1]
        w1, w2 = self.w[0], self.w[1]
        if abs(w2) > 1e-4:
            y_start = (offset - self.b - (w1 * x_start)) / w2
            y_end = (offset - self.b - (w1 * x_end)) / w2
            p1 = self.axes.c2p(x_start, y_start)
            p2 = self.axes.c2p(x_end, y_end)
        else:
            x_val = (offset - self.b) / (w1 if abs(w1) > 1e-5 else 1.0)
            p1 = self.axes.c2p(x_val, self.axes.y_range[0])
            p2 = self.axes.c2p(x_val, self.axes.y_range[1])
        return p1, p2

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup(self.axes.manim_object)

        # Draw data points
        for idx, (pt, label) in enumerate(zip(self.X, self.y, strict=False)):
            pos = self.axes.c2p(pt[0], pt[1])
            c = active_theme.colors.primary if label <= 0 else active_theme.colors.accent
            dot = manim.Dot(pos, radius=0.08, color=c)
            group.add(dot)

            # Highlight support vectors
            if idx in self.sv_indices:
                ring = manim.Circle(
                    radius=0.16, color=active_theme.colors.warning, stroke_width=2.5
                )
                ring.move_to(pos)
                group.add(ring)

        # Hyperplane and margin lines
        p1, p2 = self._get_line_endpoints(0.0)
        group.add(manim.Line(p1, p2, color=active_theme.colors.secondary, stroke_width=3.0))

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for SVM margins and support vectors."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create data points
        scatter_group = manim.VGroup(self.axes.manim_object)
        dots: list[manim.Dot] = []
        for pt, label in zip(self.X, self.y, strict=False):
            pos = self.axes.c2p(pt[0], pt[1])
            c = active_theme.colors.primary if label <= 0 else active_theme.colors.accent
            dot = manim.Dot(pos, radius=0.08, color=c)
            dots.append(dot)
            scatter_group.add(dot)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(scatter_group),
                run_time=0.8,
                name="create_svm_dataset",
            )
        )

        # 2. Highlight support vectors
        sv_group = manim.VGroup()
        for idx in self.sv_indices:
            pt = self.X[idx]
            pos = self.axes.c2p(pt[0], pt[1])
            ring = manim.Circle(radius=0.18, color=active_theme.colors.warning, stroke_width=2.5)
            ring.move_to(pos)
            sv_group.add(ring)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(sv_group),
                run_time=0.5,
                name="highlight_support_vectors",
            )
        )

        # 3. Animate separating hyperplane and margin boundaries
        hp_p1, hp_p2 = self._get_line_endpoints(0.0)
        hyperplane = manim.Line(hp_p1, hp_p2, color=active_theme.colors.secondary, stroke_width=3.0)

        pos_p1, pos_p2 = self._get_line_endpoints(1.0)
        pos_margin = manim.DashedLine(
            pos_p1, pos_p2, color=active_theme.colors.accent, stroke_width=2.0
        )

        neg_p1, neg_p2 = self._get_line_endpoints(-1.0)
        neg_margin = manim.DashedLine(
            neg_p1, neg_p2, color=active_theme.colors.primary, stroke_width=2.0
        )

        lines_group = manim.VGroup(hyperplane, pos_margin, neg_margin)
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(lines_group),
                run_time=0.8,
                name="create_hyperplane_and_margins",
            )
        )

        return animations


def svm(
    X: Sequence[Sequence[float]] | np.ndarray,
    y: Sequence[int | float] | np.ndarray,
) -> list[Animation]:
    """One-call functional API to animate Support Vector Machine classification."""
    viz = SVMVisualizer(X, y)
    return viz.animate()


__all__ = [
    "HardMarginSVMModel",
    "SVMVisualizer",
    "svm",
]
