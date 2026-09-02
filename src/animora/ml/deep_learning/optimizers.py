"""Gradient descent optimizer variants: SGD, Momentum, and Adam."""

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


class BaseOptimizerModel:
    """Base computational optimizer with numerical gradient computation and trace tracking."""

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
        """Compute numerical central difference gradient (or analytical if provided)."""
        if self.grad_fn is not None:
            g = self.grad_fn(x, y)
            return float(g[0]), float(g[1])

        df_dx = (self.loss_fn(x + self.h, y) - self.loss_fn(x - self.h, y)) / (2.0 * self.h)
        df_dy = (self.loss_fn(x, y + self.h) - self.loss_fn(x, y - self.h)) / (2.0 * self.h)
        return float(df_dx), float(df_dy)

    def optimize(self) -> list[tuple[float, float, float]]:
        """Run optimization and return list of (x, y, loss) trajectory points."""
        raise NotImplementedError


class SGDOptimizerModel(BaseOptimizerModel):
    """Standard Stochastic Gradient Descent update rule."""

    def optimize(self) -> list[tuple[float, float, float]]:
        self.trace = MLTrace()
        curr_x, curr_y = self.start
        trajectory: list[tuple[float, float, float]] = []

        for step_idx in range(self.steps + 1):
            curr_loss = float(self.loss_fn(curr_x, curr_y))
            gx, gy = self.compute_gradient(curr_x, curr_y)

            self.trace.record(
                name="step",
                description=(
                    f"SGD Step {step_idx}: pos=({curr_x:.4f}, {curr_y:.4f}), loss={curr_loss:.4f}"
                ),
                step_idx=step_idx,
                position=(curr_x, curr_y),
                loss=curr_loss,
                gradient=(gx, gy),
            )
            trajectory.append((curr_x, curr_y, curr_loss))

            if step_idx < self.steps:
                curr_x -= self.learning_rate * gx
                curr_y -= self.learning_rate * gy

        return trajectory


class MomentumOptimizerModel(BaseOptimizerModel):
    """Gradient Descent with Polyak Momentum for accelerated convergence across ravines."""

    def __init__(
        self,
        loss_fn: Callable[[float, float], float],
        start: tuple[float, float] | Sequence[float] | np.ndarray,
        *,
        learning_rate: float = 0.05,
        momentum: float = 0.85,
        steps: int = 25,
        grad_fn: Callable[[float, float], tuple[float, float]] | None = None,
    ) -> None:
        super().__init__(loss_fn, start, learning_rate=learning_rate, steps=steps, grad_fn=grad_fn)
        self.momentum = float(momentum)

    def optimize(self) -> list[tuple[float, float, float]]:
        self.trace = MLTrace()
        curr_x, curr_y = self.start
        vx, vy = 0.0, 0.0
        trajectory: list[tuple[float, float, float]] = []

        for step_idx in range(self.steps + 1):
            curr_loss = float(self.loss_fn(curr_x, curr_y))
            gx, gy = self.compute_gradient(curr_x, curr_y)

            self.trace.record(
                name="step",
                description=(
                    f"Momentum Step {step_idx}: pos=({curr_x:.4f}, {curr_y:.4f}), "
                    f"v=({vx:.4f}, {vy:.4f}), loss={curr_loss:.4f}"
                ),
                step_idx=step_idx,
                position=(curr_x, curr_y),
                velocity=(vx, vy),
                loss=curr_loss,
                gradient=(gx, gy),
            )
            trajectory.append((curr_x, curr_y, curr_loss))

            if step_idx < self.steps:
                vx = (self.momentum * vx) + (self.learning_rate * gx)
                vy = (self.momentum * vy) + (self.learning_rate * gy)
                curr_x -= vx
                curr_y -= vy

        return trajectory


class AdamOptimizerModel(BaseOptimizerModel):
    """Adaptive Moment Estimation (Adam) optimizer with 1st/2nd moment bias corrections."""

    def __init__(
        self,
        loss_fn: Callable[[float, float], float],
        start: tuple[float, float] | Sequence[float] | np.ndarray,
        *,
        learning_rate: float = 0.2,
        beta1: float = 0.9,
        beta2: float = 0.999,
        epsilon: float = 1e-8,
        steps: int = 25,
        grad_fn: Callable[[float, float], tuple[float, float]] | None = None,
    ) -> None:
        super().__init__(loss_fn, start, learning_rate=learning_rate, steps=steps, grad_fn=grad_fn)
        self.beta1 = float(beta1)
        self.beta2 = float(beta2)
        self.epsilon = float(epsilon)

    def optimize(self) -> list[tuple[float, float, float]]:
        self.trace = MLTrace()
        curr_x, curr_y = self.start
        m_x, m_y = 0.0, 0.0
        v_x, v_y = 0.0, 0.0
        trajectory: list[tuple[float, float, float]] = []

        for step_idx in range(self.steps + 1):
            curr_loss = float(self.loss_fn(curr_x, curr_y))
            gx, gy = self.compute_gradient(curr_x, curr_y)

            self.trace.record(
                name="step",
                description=(
                    f"Adam Step {step_idx}: pos=({curr_x:.4f}, {curr_y:.4f}), loss={curr_loss:.4f}"
                ),
                step_idx=step_idx,
                position=(curr_x, curr_y),
                m=(m_x, m_y),
                v=(v_x, v_y),
                loss=curr_loss,
                gradient=(gx, gy),
            )
            trajectory.append((curr_x, curr_y, curr_loss))

            if step_idx < self.steps:
                t = step_idx + 1
                # Update biased first moment estimate
                m_x = (self.beta1 * m_x) + ((1.0 - self.beta1) * gx)
                m_y = (self.beta1 * m_y) + ((1.0 - self.beta1) * gy)
                # Update biased second raw moment estimate
                v_x = (self.beta2 * v_x) + ((1.0 - self.beta2) * (gx**2))
                v_y = (self.beta2 * v_y) + ((1.0 - self.beta2) * (gy**2))

                # Compute bias-corrected estimates
                m_hat_x = m_x / (1.0 - (self.beta1**t))
                m_hat_y = m_y / (1.0 - (self.beta1**t))
                v_hat_x = v_x / (1.0 - (self.beta2**t))
                v_hat_y = v_y / (1.0 - (self.beta2**t))

                curr_x -= (self.learning_rate * m_hat_x) / (np.sqrt(v_hat_x) + self.epsilon)
                curr_y -= (self.learning_rate * m_hat_y) / (np.sqrt(v_hat_y) + self.epsilon)

        return trajectory


class OptimizerVisualizer(MLComponent):
    """Renders the optimization trajectory over a 2D contour surface."""

    def __init__(
        self,
        model: BaseOptimizerModel,
        *,
        x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.model = model
        self.trajectory = self.model.optimize()
        self.surface = SurfacePlot(fn=self.model.loss_fn, x_range=x_range, y_range=y_range)
        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup(self.surface.manim_object)

        start_pt = self.surface.c2p(self.model.start[0], self.model.start[1])
        dot = manim.Dot(start_pt, radius=0.1, color=active_theme.colors.accent)
        group.add(dot)
        return group

    def animate(self) -> list[Animation]:
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Surface create
        animations.append(self.surface.animate_create())

        # 2. Sequential trail step animation
        start_pt = self.surface.c2p(self.model.start[0], self.model.start[1])
        tracker_dot = manim.Dot(start_pt, radius=0.1, color=active_theme.colors.accent)

        for k in range(len(self.trajectory) - 1):
            p1 = self.surface.c2p(self.trajectory[k][0], self.trajectory[k][1])
            p2 = self.surface.c2p(self.trajectory[k + 1][0], self.trajectory[k + 1][1])

            step_line = manim.Line(p1, p2, color=active_theme.colors.primary, stroke_width=2.5)

            anim_move = manim.AnimationGroup(
                manim.Create(step_line),
                tracker_dot.animate.move_to(p2),
            )

            animations.append(
                Animation(
                    component=self,
                    manim_animation=anim_move,
                    run_time=0.15,
                    name=f"optim_step_{k}",
                )
            )

        return animations


def sgd(
    loss_fn: Callable[[float, float], float],
    start: tuple[float, float] | Sequence[float] | np.ndarray = (2.5, 2.5),
    *,
    learning_rate: float = 0.1,
    steps: int = 20,
    x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
    y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
) -> list[Animation]:
    """One-call functional API to animate Stochastic Gradient Descent."""
    model = SGDOptimizerModel(loss_fn, start=start, learning_rate=learning_rate, steps=steps)
    viz = OptimizerVisualizer(model, x_range=x_range, y_range=y_range)
    return viz.animate()


def momentum(
    loss_fn: Callable[[float, float], float],
    start: tuple[float, float] | Sequence[float] | np.ndarray = (2.5, 2.5),
    *,
    learning_rate: float = 0.05,
    momentum: float = 0.85,
    steps: int = 20,
    x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
    y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
) -> list[Animation]:
    """One-call functional API to animate Gradient Descent with Momentum."""
    model = MomentumOptimizerModel(
        loss_fn, start=start, learning_rate=learning_rate, momentum=momentum, steps=steps
    )
    viz = OptimizerVisualizer(model, x_range=x_range, y_range=y_range)
    return viz.animate()


def adam(
    loss_fn: Callable[[float, float], float],
    start: tuple[float, float] | Sequence[float] | np.ndarray = (2.5, 2.5),
    *,
    learning_rate: float = 0.2,
    beta1: float = 0.9,
    beta2: float = 0.999,
    steps: int = 20,
    x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
    y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
) -> list[Animation]:
    """One-call functional API to animate Adam optimizer."""
    model = AdamOptimizerModel(
        loss_fn, start=start, learning_rate=learning_rate, beta1=beta1, beta2=beta2, steps=steps
    )
    viz = OptimizerVisualizer(model, x_range=x_range, y_range=y_range)
    return viz.animate()


__all__ = [
    "AdamOptimizerModel",
    "BaseOptimizerModel",
    "MomentumOptimizerModel",
    "OptimizerVisualizer",
    "SGDOptimizerModel",
    "adam",
    "momentum",
    "sgd",
]
