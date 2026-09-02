"""K-Means clustering model, visualizer, and one-call animation API."""

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


class KMeansModel:
    """Pure computational Lloyd's K-Means clustering algorithm with iteration tracing."""

    def __init__(
        self,
        data: Sequence[Sequence[float]] | np.ndarray,
        k: int = 3,
        *,
        max_iters: int = 10,
        initial_centroids: Sequence[Sequence[float]] | np.ndarray | None = None,
        random_state: int = 42,
    ) -> None:
        self.data = np.asarray(data, dtype=float)
        if self.data.ndim != 2 or self.data.shape[1] != 2:
            raise ValueError("data must be a 2D array of shape (N, 2).")
        self.k = max(1, min(int(k), len(self.data)))
        self.max_iters = max(1, int(max_iters))
        self.random_state = random_state
        self.trace = MLTrace()

        if initial_centroids is not None:
            self.initial_centroids = np.asarray(initial_centroids, dtype=float)
        else:
            rng = np.random.default_rng(self.random_state)
            indices = rng.choice(len(self.data), size=self.k, replace=False)
            self.initial_centroids = self.data[indices].copy()

    def fit(self) -> list[dict[str, Any]]:
        """Run Lloyd's algorithm iterations and record step events to MLTrace."""
        self.trace = MLTrace()
        centroids = self.initial_centroids.copy()
        history: list[dict[str, Any]] = []

        for iteration in range(self.max_iters):
            # 1. Assignment step
            diff = self.data[:, np.newaxis, :] - centroids[np.newaxis, :, :]
            dists = np.linalg.norm(diff, axis=2)
            assignments = np.argmin(dists, axis=1)

            # Compute inertia (sum of squared distances)
            inertia = float(np.sum(np.min(dists, axis=1) ** 2))

            history_entry = {
                "iteration": iteration,
                "centroids": centroids.copy(),
                "assignments": assignments.copy(),
                "inertia": inertia,
            }
            history.append(history_entry)

            self.trace.record(
                name="iteration",
                description=f"Iter {iteration}: inertia={inertia:.3f}",
                iteration=iteration,
                centroids=[tuple(c) for c in centroids],
                assignments=assignments.tolist(),
                inertia=inertia,
            )

            # 2. Update step
            new_centroids = np.zeros_like(centroids)
            for cluster_idx in range(self.k):
                cluster_pts = self.data[assignments == cluster_idx]
                if len(cluster_pts) > 0:
                    new_centroids[cluster_idx] = np.mean(cluster_pts, axis=0)
                else:
                    new_centroids[cluster_idx] = centroids[cluster_idx]

            # Check convergence
            if np.allclose(centroids, new_centroids, atol=1e-4):
                break

            centroids = new_centroids

        return history


class KMeansVisualizer(MLComponent):
    """Component visualizer for K-Means point recoloring and centroid movement."""

    def __init__(
        self,
        data: Sequence[Sequence[float]] | np.ndarray,
        k: int = 3,
        *,
        max_iters: int = 10,
        initial_centroids: Sequence[Sequence[float]] | np.ndarray | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.data = np.asarray(data, dtype=float)
        self.k = int(k)
        self.model = KMeansModel(
            self.data, k=self.k, max_iters=max_iters, initial_centroids=initial_centroids
        )
        self.history = self.model.fit()

        x_min, x_max = float(np.min(self.data[:, 0])), float(np.max(self.data[:, 0]))
        y_min, y_max = float(np.min(self.data[:, 1])), float(np.max(self.data[:, 1]))
        x_pad = max(1.0, 0.25 * (x_max - x_min))
        y_pad = max(1.0, 0.25 * (y_max - y_min))

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

        # Draw data points with neutral color
        for pt in self.data:
            pos = self.axes.c2p(pt[0], pt[1])
            dot = manim.Dot(pos, radius=0.07, color=active_theme.colors.text_muted)
            group.add(dot)

        # Draw initial centroids
        init_centroids = self.history[0]["centroids"]
        for c in init_centroids:
            pos = self.axes.c2p(c[0], c[1])
            cross = manim.Cross(stroke_color=active_theme.colors.accent, stroke_width=4.0)
            cross.scale(0.15).move_to(pos)
            group.add(cross)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for K-Means clustering iterations."""
        active_theme = get_active_theme()
        cluster_colors = [
            active_theme.colors.primary,
            active_theme.colors.accent,
            active_theme.colors.secondary,
            active_theme.colors.success,
            "#EC4899",
            "#8B5CF6",
        ]

        animations: list[Animation] = []

        # 1. Spawn axes and initial points
        point_dots: list[manim.Dot] = []
        scatter_group = manim.VGroup(self.axes.manim_object)
        for pt in self.data:
            pos = self.axes.c2p(pt[0], pt[1])
            dot = manim.Dot(pos, radius=0.07, color=active_theme.colors.text_muted)
            point_dots.append(dot)
            scatter_group.add(dot)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(scatter_group),
                run_time=0.8,
                name="create_kmeans_data",
            )
        )

        # 2. Spawn initial centroids
        centroid_mobjects: list[manim.Mobject] = []
        centroid_group = manim.VGroup()
        init_centroids = self.history[0]["centroids"]
        for idx, c in enumerate(init_centroids):
            pos = self.axes.c2p(c[0], c[1])
            color = cluster_colors[idx % len(cluster_colors)]
            c_marker = manim.Cross(stroke_color=color, stroke_width=4.5)
            c_marker.scale(0.18).move_to(pos)
            centroid_mobjects.append(c_marker)
            centroid_group.add(c_marker)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(centroid_group),
                run_time=0.5,
                name="init_centroids",
            )
        )

        # 3. Animate each iteration
        for iter_idx, entry in enumerate(self.history):
            assignments = entry["assignments"]

            # Animate point recoloring according to cluster
            recolor_anims = []
            for pt_idx, cluster_id in enumerate(assignments):
                target_color = cluster_colors[cluster_id % len(cluster_colors)]
                recolor_anims.append(point_dots[pt_idx].animate.set_color(target_color))

            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.AnimationGroup(*recolor_anims),
                    run_time=0.3,
                    name=f"assign_points_iter_{iter_idx}",
                )
            )

            # Move centroids to new positions
            if iter_idx + 1 < len(self.history):
                next_centroids = self.history[iter_idx + 1]["centroids"]
                move_anims = []
                for c_idx in range(self.k):
                    target_pos = self.axes.c2p(next_centroids[c_idx][0], next_centroids[c_idx][1])
                    move_anims.append(centroid_mobjects[c_idx].animate.move_to(target_pos))

                animations.append(
                    Animation(
                        component=self,
                        manim_animation=manim.AnimationGroup(*move_anims),
                        run_time=0.4,
                        name=f"shift_centroids_iter_{iter_idx}",
                    )
                )

        return animations


def kmeans(
    data: Sequence[Sequence[float]] | np.ndarray,
    k: int = 3,
    *,
    max_iters: int = 10,
    initial_centroids: Sequence[Sequence[float]] | np.ndarray | None = None,
) -> list[Animation]:
    """One-call functional API to animate K-Means clustering algorithm."""
    viz = KMeansVisualizer(data, k=k, max_iters=max_iters, initial_centroids=initial_centroids)
    return viz.animate()


__all__ = [
    "KMeansModel",
    "KMeansVisualizer",
    "kmeans",
]
