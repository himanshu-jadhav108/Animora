"""Principal Component Analysis (PCA) model, visualizer, and one-call animation API."""

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


class PCAModel:
    """Mathematical Principal Component Analysis computing exact SVD/eigendecomposition."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        n_components: int = 1,
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        if self.X.ndim != 2 or self.X.shape[1] != 2:
            raise ValueError("X must be a 2D array of shape (N, 2).")
        self.n_components = min(int(n_components), self.X.shape[1])
        self.trace = MLTrace()

        # Fit
        self.mean = np.mean(self.X, axis=0)
        self.X_centered = self.X - self.mean
        cov = np.cov(self.X_centered, rowvar=False)

        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        # Sort in descending order
        idx = np.argsort(eigenvalues)[::-1]
        self.eigenvalues = eigenvalues[idx]
        self.components = eigenvectors[:, idx].T  # Each row is a principal component

        total_var = float(np.sum(self.eigenvalues))
        self.explained_variance_ratio = (
            self.eigenvalues / total_var if total_var > 1e-9 else np.ones_like(self.eigenvalues)
        )

        # Compute projections onto 1st principal component
        v1 = self.components[0]
        projections_1d = np.dot(self.X_centered, v1)
        self.projected_points = self.mean + (projections_1d[:, np.newaxis] * v1)

        self.trace.record(
            name="pca_fit",
            description=(
                f"PCA: PC1={self.components[0]}, var_ratio={self.explained_variance_ratio[0]:.3f}"
            ),
            mean=tuple(self.mean),
            components=[tuple(c) for c in self.components],
            eigenvalues=tuple(self.eigenvalues),
            explained_variance_ratio=tuple(self.explained_variance_ratio),
        )


class PCAVisualizer(MLComponent):
    """Component visualizer for 2D PCA principal axes and data projections."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        *,
        n_components: int = 1,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        self.model = PCAModel(self.X, n_components=n_components)

        x_min, x_max = float(np.min(self.X[:, 0])), float(np.max(self.X[:, 0]))
        y_min, y_max = float(np.min(self.X[:, 1])), float(np.max(self.X[:, 1]))
        x_pad = max(1.0, 0.3 * (x_max - x_min))
        y_pad = max(1.0, 0.3 * (y_max - y_min))

        self.axes = Axes(
            x_range=(x_min - x_pad, x_max + x_pad, (x_max - x_min + 2 * x_pad) / 5),
            y_range=(y_min - y_pad, y_max + y_pad, (y_max - y_min + 2 * y_pad) / 5),
            x_length=7.0,
            y_length=5.0,
        )

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup(self.axes.manim_object)

        # Scatter points
        for pt in self.X:
            pos = self.axes.c2p(pt[0], pt[1])
            dot = manim.Dot(pos, radius=0.08, color=active_theme.colors.primary)
            group.add(dot)

        # Principal axes arrows
        mean_p = self.axes.c2p(self.model.mean[0], self.model.mean[1])
        v1 = self.model.components[0]
        scale1 = 1.5 * np.sqrt(max(0.1, self.model.eigenvalues[0]))
        target1 = self.model.mean + (v1 * scale1)
        end1 = self.axes.c2p(target1[0], target1[1])
        arrow1 = manim.Arrow(mean_p, end1, color=active_theme.colors.accent, buff=0.0)
        group.add(arrow1)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for PCA axes and orthogonal projections."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create data points and axes
        scatter_group = manim.VGroup(self.axes.manim_object)
        data_dots: list[manim.Dot] = []
        for pt in self.X:
            pos = self.axes.c2p(pt[0], pt[1])
            dot = manim.Dot(pos, radius=0.08, color=active_theme.colors.primary)
            data_dots.append(dot)
            scatter_group.add(dot)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(scatter_group),
                run_time=0.8,
                name="create_pca_dataset",
            )
        )

        # 2. Animate principal component arrows radiating from centroid
        mean_p = self.axes.c2p(self.model.mean[0], self.model.mean[1])
        center_dot = manim.Dot(mean_p, radius=0.1, color=active_theme.colors.warning)

        # PC1 arrow
        v1 = self.model.components[0]
        scale1 = 1.8 * np.sqrt(max(0.1, self.model.eigenvalues[0]))
        target1 = self.model.mean + (v1 * scale1)
        end1 = self.axes.c2p(target1[0], target1[1])
        arrow1 = manim.Arrow(
            mean_p, end1, color=active_theme.colors.accent, buff=0.0, stroke_width=3.5
        )

        # PC2 arrow
        v2 = self.model.components[1]
        scale2 = 1.8 * np.sqrt(max(0.1, self.model.eigenvalues[1]))
        target2 = self.model.mean + (v2 * scale2)
        end2 = self.axes.c2p(target2[0], target2[1])
        arrow2 = manim.Arrow(
            mean_p, end2, color=active_theme.colors.secondary, buff=0.0, stroke_width=2.5
        )

        pc_group = manim.VGroup(center_dot, arrow1, arrow2)
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(pc_group),
                run_time=0.7,
                name="show_principal_components",
            )
        )

        # 3. Animate orthogonal projections onto PC1
        proj_group = manim.VGroup()
        for idx in range(len(self.X)):
            orig_p = self.axes.c2p(self.X[idx, 0], self.X[idx, 1])
            proj_data = self.model.projected_points[idx]
            proj_p = self.axes.c2p(proj_data[0], proj_data[1])

            proj_line = manim.DashedLine(
                orig_p, proj_p, color=active_theme.colors.border, stroke_width=1.5
            )
            proj_dot = manim.Dot(proj_p, radius=0.06, color=active_theme.colors.accent)
            proj_group.add(proj_line, proj_dot)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(proj_group),
                run_time=0.8,
                name="project_onto_pc1",
            )
        )

        return animations


def pca(
    X: Sequence[Sequence[float]] | np.ndarray,
    *,
    n_components: int = 1,
) -> list[Animation]:
    """One-call functional API to animate Principal Component Analysis."""
    viz = PCAVisualizer(X, n_components=n_components)
    return viz.animate()


__all__ = [
    "PCAModel",
    "PCAVisualizer",
    "pca",
]
