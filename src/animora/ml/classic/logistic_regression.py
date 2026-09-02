"""Logistic regression model, visualizer, and one-call decision boundary animation API."""

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


class LogisticRegressionModel:
    """Binary logistic regression model with sigmoid activation and cross-entropy tracing."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        y: Sequence[int | float] | np.ndarray,
        *,
        learning_rate: float = 0.2,
        steps: int = 15,
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        self.y = np.asarray(y, dtype=float)
        if self.X.ndim != 2 or self.X.shape[1] != 2:
            raise ValueError("X must be a 2D array with shape (N, 2).")
        if len(self.X) != len(self.y) or len(self.X) < 2:
            raise ValueError("X and y must have equal length with at least 2 samples.")

        self.learning_rate = float(learning_rate)
        self.steps = max(1, int(steps))
        self.trace = MLTrace()

    @staticmethod
    def sigmoid(z: np.ndarray) -> np.ndarray:
        """Numerically stable sigmoid function."""
        res: np.ndarray = np.asarray(
            np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)), np.exp(z) / (1.0 + np.exp(z))),
            dtype=float,
        )
        return res

    def fit(self) -> list[tuple[float, float, float, float]]:
        """Run gradient descent optimization and record decision boundary parameters."""
        self.trace = MLTrace()
        n = len(self.X)

        w = np.zeros(2, dtype=float)
        b = 0.0
        trajectory: list[tuple[float, float, float, float]] = []

        for step_idx in range(self.steps + 1):
            z = np.dot(self.X, w) + b
            y_hat = self.sigmoid(z)
            eps = 1e-9
            loss = float(
                -np.mean(self.y * np.log(y_hat + eps) + (1.0 - self.y) * np.log(1.0 - y_hat + eps))
            )

            self.trace.record(
                name="step",
                description=(
                    f"Step {step_idx}: w=[{w[0]:.3f}, {w[1]:.3f}], b={b:.3f}, loss={loss:.3f}"
                ),
                step_idx=step_idx,
                weights=(float(w[0]), float(w[1])),
                bias=float(b),
                loss=loss,
            )
            trajectory.append((float(w[0]), float(w[1]), float(b), loss))

            if step_idx < self.steps:
                error = y_hat - self.y
                grad_w = np.dot(self.X.T, error) / n
                grad_b = float(np.mean(error))
                w -= self.learning_rate * grad_w
                b -= self.learning_rate * grad_b

        return trajectory


class LogisticRegressionVisualizer(MLComponent):
    """Component visualizer for 2D classification points and decision boundary."""

    def __init__(
        self,
        X: Sequence[Sequence[float]] | np.ndarray,
        y: Sequence[int | float] | np.ndarray,
        *,
        steps: int = 15,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.X = np.asarray(X, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.model = LogisticRegressionModel(self.X, self.y, steps=steps)
        self.trajectory = self.model.fit()

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

    def _get_boundary_endpoints(
        self, w1: float, w2: float, b: float
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute visual line segment endpoints for w1*x + w2*y + b = 0."""
        x_start, x_end = self.axes.x_range[0], self.axes.x_range[1]
        if abs(w2) > 1e-4:
            y_start = -(w1 * x_start + b) / w2
            y_end = -(w1 * x_end + b) / w2
            p1 = self.axes.c2p(x_start, y_start)
            p2 = self.axes.c2p(x_end, y_end)
        else:
            # Vertical line x = -b / w1
            x_val = -b / (w1 if abs(w1) > 1e-5 else 1.0)
            p1 = self.axes.c2p(x_val, self.axes.y_range[0])
            p2 = self.axes.c2p(x_val, self.axes.y_range[1])
        return p1, p2

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup(self.axes.manim_object)

        # Draw scatter points colored by binary class
        for pt, label in zip(self.X, self.y, strict=False):
            pos = self.axes.c2p(pt[0], pt[1])
            c = active_theme.colors.primary if label == 0 else active_theme.colors.accent
            dot = manim.Dot(pos, radius=0.08, color=c)
            group.add(dot)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for logistic regression boundary fitting."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Scatter points and axes
        scatter_group = manim.VGroup(self.axes.manim_object)
        for pt, label in zip(self.X, self.y, strict=False):
            pos = self.axes.c2p(pt[0], pt[1])
            c = active_theme.colors.primary if label == 0 else active_theme.colors.accent
            dot = manim.Dot(pos, radius=0.08, color=c)
            scatter_group.add(dot)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(scatter_group),
                run_time=0.8,
                name="create_classification_data",
            )
        )

        # 2. Initial boundary line
        w1, w2, b, _ = self.trajectory[0]
        p1, p2 = self._get_boundary_endpoints(w1, w2, b)
        boundary_line = manim.Line(p1, p2, color=active_theme.colors.secondary, stroke_width=3.0)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(boundary_line),
                run_time=0.4,
                name="init_boundary_line",
            )
        )

        # 3. Animate convergence
        for step_idx in range(1, len(self.trajectory)):
            w1_n, w2_n, b_n, _ = self.trajectory[step_idx]
            next_p1, next_p2 = self._get_boundary_endpoints(w1_n, w2_n, b_n)
            target_line = manim.Line(
                next_p1, next_p2, color=active_theme.colors.secondary, stroke_width=3.0
            )

            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.Transform(boundary_line, target_line),
                    run_time=0.15,
                    name=f"boundary_step_{step_idx}",
                )
            )

        return animations


def logistic_regression(
    X: Sequence[Sequence[float]] | np.ndarray,
    y: Sequence[int | float] | np.ndarray,
    *,
    steps: int = 15,
) -> list[Animation]:
    """One-call functional API to animate logistic regression decision boundary fitting."""
    viz = LogisticRegressionVisualizer(X, y, steps=steps)
    return viz.animate()


__all__ = [
    "LogisticRegressionModel",
    "LogisticRegressionVisualizer",
    "logistic_regression",
]
