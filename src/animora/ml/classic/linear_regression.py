"""Linear regression model, visualizer, and one-call animation API."""

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


class LinearRegressionModel:
    """Mathematical linear regression solver with gradient-descent iteration tracing."""

    def __init__(
        self,
        x: Sequence[float] | np.ndarray,
        y: Sequence[float] | np.ndarray,
        *,
        learning_rate: float = 0.05,
        steps: int = 15,
    ) -> None:
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        if len(self.x) != len(self.y) or len(self.x) < 2:
            raise ValueError("x and y must have equal lengths with at least 2 points.")

        self.learning_rate = float(learning_rate)
        self.steps = max(1, int(steps))
        self.trace = MLTrace()

        # Closed form least-squares solution (reference ground truth)
        x_mean = float(np.mean(self.x))
        y_mean = float(np.mean(self.y))
        denom = float(np.sum((self.x - x_mean) ** 2))
        if abs(denom) < 1e-9:
            self.optimal_w = 0.0
            self.optimal_b = y_mean
        else:
            self.optimal_w = float(np.sum((self.x - x_mean) * (self.y - y_mean)) / denom)
            self.optimal_b = float(y_mean - (self.optimal_w * x_mean))

    def fit_gradient_descent(self) -> list[tuple[float, float, float]]:
        """Run gradient descent fitting and record iteration steps to MLTrace."""
        self.trace = MLTrace()
        n = len(self.x)

        # Normalize x for numerically stable optimization
        x_min, x_max = float(np.min(self.x)), float(np.max(self.x))
        span = x_max - x_min if abs(x_max - x_min) > 1e-6 else 1.0
        x_norm = (self.x - x_min) / span

        w, b = 0.0, float(np.mean(self.y))
        trajectory: list[tuple[float, float, float]] = []

        for step_idx in range(self.steps + 1):
            y_pred = (w * x_norm) + b
            mse = float(np.mean((self.y - y_pred) ** 2))

            # Denormalize slope back to original data coordinates
            actual_w = w / span
            actual_b = b - (w * x_min / span)

            self.trace.record(
                name="step",
                description=f"Step {step_idx}: w={actual_w:.3f}, b={actual_b:.3f}, mse={mse:.3f}",
                step_idx=step_idx,
                slope=actual_w,
                intercept=actual_b,
                mse=mse,
            )
            trajectory.append((actual_w, actual_b, mse))

            if step_idx < self.steps:
                grad_w = float(-2.0 / n * np.sum(x_norm * (self.y - y_pred)))
                grad_b = float(-2.0 / n * np.sum(self.y - y_pred))
                w -= self.learning_rate * grad_w
                b -= self.learning_rate * grad_b

        # Final step aligns with optimal closed-form solution
        final_mse = float(np.mean((self.y - ((self.optimal_w * self.x) + self.optimal_b)) ** 2))
        trajectory.append((self.optimal_w, self.optimal_b, final_mse))
        return trajectory


class LinearRegressionVisualizer(MLComponent):
    """Component orchestrating 2D data points, coordinate axes, and fitting line."""

    def __init__(
        self,
        x: Sequence[float] | np.ndarray,
        y: Sequence[float] | np.ndarray,
        *,
        steps: int = 12,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.x_vals = np.asarray(x, dtype=float)
        self.y_vals = np.asarray(y, dtype=float)
        self.model = LinearRegressionModel(self.x_vals, self.y_vals, steps=steps)
        self.trajectory = self.model.fit_gradient_descent()

        # Build coordinate axes with padding
        x_min, x_max = float(np.min(self.x_vals)), float(np.max(self.x_vals))
        y_min, y_max = float(np.min(self.y_vals)), float(np.max(self.y_vals))
        x_pad = max(1.0, 0.2 * (x_max - x_min))
        y_pad = max(1.0, 0.2 * (y_max - y_min))

        self.axes = Axes(
            x_range=(x_min - x_pad, x_max + x_pad, (x_max - x_min + 2 * x_pad) / 5),
            y_range=(y_min - y_pad, y_max + y_pad, (y_max - y_min + 2 * y_pad) / 5),
            x_length=7.0,
            y_length=5.0,
        )

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup()
        group.add(self.axes.manim_object)

        # Plot data points
        for xi, yi in zip(self.x_vals, self.y_vals, strict=False):
            pt = self.axes.c2p(xi, yi)
            dot = manim.Dot(pt, radius=0.08, color=active_theme.colors.secondary)
            group.add(dot)

        # Initial horizontal line
        w0, b0, _ = self.trajectory[0]
        x_start, x_end = self.axes.x_range[0], self.axes.x_range[1]
        line = manim.Line(
            self.axes.c2p(x_start, (w0 * x_start) + b0),
            self.axes.c2p(x_end, (w0 * x_end) + b0),
            color=active_theme.colors.primary,
            stroke_width=3.0,
        )
        group.add(line)
        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for linear regression fitting."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create axes and scatter dots
        scatter_group = manim.VGroup(self.axes.manim_object)
        for xi, yi in zip(self.x_vals, self.y_vals, strict=False):
            pt = self.axes.c2p(xi, yi)
            dot = manim.Dot(pt, radius=0.08, color=active_theme.colors.secondary)
            scatter_group.add(dot)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(scatter_group),
                run_time=0.8,
                name="create_data_and_axes",
            )
        )

        # 2. Animate line fitting steps
        x_start, x_end = self.axes.x_range[0], self.axes.x_range[1]
        w0, b0, _ = self.trajectory[0]
        current_line = manim.Line(
            self.axes.c2p(x_start, (w0 * x_start) + b0),
            self.axes.c2p(x_end, (w0 * x_end) + b0),
            color=active_theme.colors.primary,
            stroke_width=3.0,
        )
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(current_line),
                run_time=0.4,
                name="init_fit_line",
            )
        )

        # Convergence steps
        for step_idx in range(1, len(self.trajectory)):
            w_next, b_next, _ = self.trajectory[step_idx]
            target_line = manim.Line(
                self.axes.c2p(x_start, (w_next * x_start) + b_next),
                self.axes.c2p(x_end, (w_next * x_end) + b_next),
                color=active_theme.colors.primary,
                stroke_width=3.0,
            )
            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.Transform(current_line, target_line),
                    run_time=0.15,
                    name=f"fit_step_{step_idx}",
                )
            )

        return animations


def linear_regression(
    x: Sequence[float] | np.ndarray,
    y: Sequence[float] | np.ndarray,
    *,
    steps: int = 12,
) -> list[Animation]:
    """One-call functional API to animate linear regression fitting."""
    viz = LinearRegressionVisualizer(x, y, steps=steps)
    return viz.animate()


__all__ = [
    "LinearRegressionModel",
    "LinearRegressionVisualizer",
    "linear_regression",
]
