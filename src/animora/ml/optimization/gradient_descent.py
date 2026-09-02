"""Gradient descent optimization algorithm model and one-call visualizer."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.ml.surface_plot import SurfacePlot
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class GradientDescentModel:
    """Pure computational gradient descent optimizer with operation tracing.

    Computes central-difference numerical gradients (or uses supplied analytical gradient)
    and records the trajectory and loss values across iteration steps.
    """

    def __init__(
        self,
        loss_fn: Callable[[float, float], float],
        start: tuple[float, float] | Sequence[float] | np.ndarray,
        *,
        learning_rate: float = 0.1,
        steps: int = 25,
        grad_fn: Callable[[float, float], tuple[float, float]] | None = None,
        h: float = 1e-5,
    ) -> None:
        self.loss_fn = loss_fn
        self.start = (float(start[0]), float(start[1]))
        self.learning_rate = float(learning_rate)
        self.steps = max(1, int(steps))
        self.grad_fn = grad_fn
        self.h = float(h)
        self.trace = MLTrace()

    def compute_gradient(self, x: float, y: float) -> tuple[float, float]:
        """Compute the 2D gradient vector (df/dx, df/dy)."""
        if self.grad_fn is not None:
            g = self.grad_fn(x, y)
            return float(g[0]), float(g[1])

        # Central difference approximation
        df_dx = (self.loss_fn(x + self.h, y) - self.loss_fn(x - self.h, y)) / (2.0 * self.h)
        df_dy = (self.loss_fn(x, y + self.h) - self.loss_fn(x, y - self.h)) / (2.0 * self.h)
        return float(df_dx), float(df_dy)

    def optimize(self) -> list[tuple[float, float, float]]:
        """Run optimization and return list of (x, y, loss) trajectory points."""
        self.trace = MLTrace()
        curr_x, curr_y = self.start
        trajectory: list[tuple[float, float, float]] = []

        for step_idx in range(self.steps + 1):
            curr_loss = float(self.loss_fn(curr_x, curr_y))
            grad_x, grad_y = self.compute_gradient(curr_x, curr_y)

            self.trace.record(
                name="step",
                description=(
                    f"Step {step_idx}: pos=({curr_x:.4f}, {curr_y:.4f}), loss={curr_loss:.4f}"
                ),
                step_idx=step_idx,
                position=(curr_x, curr_y),
                loss=curr_loss,
                gradient=(grad_x, grad_y),
            )
            trajectory.append((curr_x, curr_y, curr_loss))

            if step_idx < self.steps:
                curr_x -= self.learning_rate * grad_x
                curr_y -= self.learning_rate * grad_y

        return trajectory


class GradientDescentVisualizer(MLComponent):
    """Component orchestrating a loss surface plot, trajectory trails, and optimizer dot."""

    def __init__(
        self,
        loss_fn: Callable[[float, float], float],
        start: tuple[float, float] | Sequence[float] | np.ndarray,
        *,
        learning_rate: float = 0.1,
        steps: int = 20,
        x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.loss_fn = loss_fn
        self.start = (float(start[0]), float(start[1]))
        self.learning_rate = float(learning_rate)
        self.steps = max(1, int(steps))
        self.x_range = x_range
        self.y_range = y_range

        self.model = GradientDescentModel(
            loss_fn=self.loss_fn,
            start=self.start,
            learning_rate=self.learning_rate,
            steps=self.steps,
        )
        self.trajectory = self.model.optimize()

        self.surface = SurfacePlot(
            fn=self.loss_fn,
            x_range=self.x_range,
            y_range=self.y_range,
        )

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        """Build initial static scene elements."""
        active_theme = get_active_theme()
        group = manim.VGroup()
        group.add(self.surface.manim_object)

        # Start point marker dot
        start_pt = self.surface.c2p(self.start[0], self.start[1])
        dot = manim.Dot(start_pt, radius=0.1, color=active_theme.colors.accent)
        group.add(dot)

        return group

    def animate(self) -> list[Animation]:
        """One-call method generating all animations for the optimization run."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create the surface plot
        animations.append(self.surface.animate_create())

        # 2. Sequential descent steps
        start_pt = self.surface.c2p(self.start[0], self.start[1])
        tracker_dot = manim.Dot(start_pt, radius=0.1, color=active_theme.colors.accent)

        for k in range(len(self.trajectory) - 1):
            p1 = self.surface.c2p(self.trajectory[k][0], self.trajectory[k][1])
            p2 = self.surface.c2p(self.trajectory[k + 1][0], self.trajectory[k + 1][1])

            step_line = manim.Line(
                p1,
                p2,
                color=active_theme.colors.primary,
                stroke_width=2.5,
            )

            # Move dot along the step and draw segment
            anim_move = manim.AnimationGroup(
                manim.Create(step_line),
                tracker_dot.animate.move_to(p2),
            )

            animations.append(
                Animation(
                    component=self,
                    manim_animation=anim_move,
                    run_time=0.15,
                    name=f"gd_step_{k}",
                )
            )

        return animations


def gradient_descent(
    loss_fn: Callable[[float, float], float],
    start: tuple[float, float] | Sequence[float] | np.ndarray = (2.5, 2.5),
    *,
    learning_rate: float = 0.1,
    steps: int = 20,
    x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
    y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
) -> list[Animation]:
    """One-call functional API for visualizing gradient descent.

    Example:
    ```python
    def loss_fn(x: float, y: float) -> float:
        return x**2 + y**2

    self.play(*gradient_descent(loss_fn, start=(2.0, 2.0), learning_rate=0.1, steps=20))
    ```
    """
    visualizer = GradientDescentVisualizer(
        loss_fn=loss_fn,
        start=start,
        learning_rate=learning_rate,
        steps=steps,
        x_range=x_range,
        y_range=y_range,
    )
    return visualizer.animate()


__all__ = [
    "GradientDescentModel",
    "GradientDescentVisualizer",
    "gradient_descent",
]
