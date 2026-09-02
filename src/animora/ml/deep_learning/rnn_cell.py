"""Recurrent Neural Network (RNN) cell model, unrolled sequential visualizer, and one-call API."""

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
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class RNNCellModel:
    """Mathematical Recurrent Neural Network unrolled sequential state machine."""

    def __init__(
        self,
        input_dim: int = 2,
        hidden_dim: int = 2,
        *,
        W_xh: np.ndarray | None = None,
        W_hh: np.ndarray | None = None,
        b_h: np.ndarray | None = None,
        random_seed: int = 42,
    ) -> None:
        self.input_dim = max(1, int(input_dim))
        self.hidden_dim = max(1, int(hidden_dim))
        self.trace = MLTrace()

        rng = np.random.default_rng(random_seed)
        self.W_xh = (
            np.asarray(W_xh, dtype=float)
            if W_xh is not None
            else rng.normal(0.0, 0.5, size=(self.hidden_dim, self.input_dim))
        )
        self.W_hh = (
            np.asarray(W_hh, dtype=float)
            if W_hh is not None
            else rng.normal(0.0, 0.5, size=(self.hidden_dim, self.hidden_dim))
        )
        self.b_h = (
            np.asarray(b_h, dtype=float)
            if b_h is not None
            else np.zeros(self.hidden_dim, dtype=float)
        )

    def forward_sequence(
        self,
        inputs: Sequence[Sequence[float]] | np.ndarray,
        h0: Sequence[float] | np.ndarray | None = None,
    ) -> list[np.ndarray]:
        """Compute sequential hidden state updates across timesteps."""
        self.trace = MLTrace()
        X = np.asarray(inputs, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.input_dim:
            raise ValueError(f"inputs must have shape (T, {self.input_dim}).")

        h_curr = (
            np.asarray(h0, dtype=float)
            if h0 is not None
            else np.zeros(self.hidden_dim, dtype=float)
        )
        hidden_states: list[np.ndarray] = [h_curr.copy()]

        for t in range(len(X)):
            x_t = X[t]
            h_next = np.tanh(np.dot(self.W_xh, x_t) + np.dot(self.W_hh, h_curr) + self.b_h)
            hidden_states.append(h_next)

            self.trace.record(
                name=f"step_{t}",
                description=f"Step t={t}: x={x_t.tolist()}, h={h_next.tolist()}",
                t=t,
                x=x_t.tolist(),
                h_prev=h_curr.tolist(),
                h_curr=h_next.tolist(),
            )
            h_curr = h_next

        return hidden_states


class RNNVisualizer(MLComponent):
    """Visualizes unrolled RNN cells with sequential hidden state propagation arrows."""

    def __init__(
        self,
        inputs: Sequence[Sequence[float]] | np.ndarray,
        *,
        hidden_dim: int = 2,
        W_xh: np.ndarray | None = None,
        W_hh: np.ndarray | None = None,
        b_h: np.ndarray | None = None,
        cell_spacing: float = 2.8,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.inputs = np.asarray(inputs, dtype=float)
        self.model = RNNCellModel(
            input_dim=self.inputs.shape[1],
            hidden_dim=hidden_dim,
            W_xh=W_xh,
            W_hh=W_hh,
            b_h=b_h,
        )
        self.hidden_states = self.model.forward_sequence(self.inputs)
        self.cell_spacing = float(cell_spacing)
        self.T = len(self.inputs)

        # Precompute positions for each unrolled timestep cell
        self.cell_centers: list[np.ndarray] = []
        for t in range(self.T):
            cx = (t - (self.T - 1) / 2.0) * self.cell_spacing
            self.cell_centers.append(np.array([cx, 0.0, 0.0]))

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup()

        for t in range(self.T):
            center = self.cell_centers[t]
            h_val = self.hidden_states[t + 1]

            # Cell box
            card = Panel(
                Text(f"h: [{h_val[0]:.2f}, {h_val[1]:.2f}]", font_size=12),
                title=f"RNN Cell t={t}",
                width=1.9,
                height=1.2,
            )
            card.move_to(center)
            group.add(card.manim_object)

            # Input arrow from bottom
            in_start = center + np.array([0.0, -1.3, 0.0])
            in_end = center + np.array([0.0, -0.65, 0.0])
            in_arrow = manim.Arrow(in_start, in_end, color=active_theme.colors.accent, buff=0.0)
            group.add(in_arrow)

            # Connecting hidden arrow to next cell
            if t < self.T - 1:
                next_center = self.cell_centers[t + 1]
                h_start = center + np.array([1.0, 0.0, 0.0])
                h_end = next_center + np.array([-1.0, 0.0, 0.0])
                h_arrow = manim.Arrow(h_start, h_end, color=active_theme.colors.primary, buff=0.0)
                group.add(h_arrow)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for unrolled sequential RNN execution."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        for t in range(self.T):
            center = self.cell_centers[t]
            h_val = self.hidden_states[t + 1]

            card = Panel(
                Text(f"h: [{h_val[0]:.2f}, {h_val[1]:.2f}]", font_size=12),
                title=f"RNN Cell t={t}",
                width=1.9,
                height=1.2,
            )
            card.move_to(center)

            in_start = center + np.array([0.0, -1.3, 0.0])
            in_end = center + np.array([0.0, -0.65, 0.0])
            in_arrow = manim.Arrow(in_start, in_end, color=active_theme.colors.accent, buff=0.0)

            step_group = manim.VGroup(card.manim_object, in_arrow)

            if t > 0:
                prev_center = self.cell_centers[t - 1]
                h_start = prev_center + np.array([1.0, 0.0, 0.0])
                h_end = center + np.array([-1.0, 0.0, 0.0])
                h_arrow = manim.Arrow(h_start, h_end, color=active_theme.colors.primary, buff=0.0)
                step_group.add(h_arrow)

            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.Create(step_group),
                    run_time=0.6,
                    name=f"unroll_step_{t}",
                )
            )

        return animations


def rnn_forward(
    inputs: Sequence[Sequence[float]] | np.ndarray,
    *,
    hidden_dim: int = 2,
    W_xh: np.ndarray | None = None,
    W_hh: np.ndarray | None = None,
    b_h: np.ndarray | None = None,
) -> list[Animation]:
    """One-call functional API to animate unrolled sequential RNN execution."""
    viz = RNNVisualizer(inputs, hidden_dim=hidden_dim, W_xh=W_xh, W_hh=W_hh, b_h=b_h)
    return viz.animate()


__all__ = [
    "RNNCellModel",
    "RNNVisualizer",
    "rnn_forward",
]
