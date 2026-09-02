"""Backpropagation gradient computation, numerical verification, and one-call visualizer."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.ml.deep_learning.neural_network import NeuralNetworkModel
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class BackpropagationModel:
    """Computes exact analytical backpropagation gradients and performs finite-difference checks."""

    def __init__(
        self,
        net: NeuralNetworkModel,
    ) -> None:
        self.net = net
        self.trace = MLTrace()

    @staticmethod
    def sigmoid_derivative(a: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid given activation a = sigmoid(z)."""
        return a * (1.0 - a)

    def backward(
        self,
        x: Sequence[float] | np.ndarray,
        y_target: Sequence[float] | np.ndarray,
    ) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """Compute backward pass returning gradients (grad_W, grad_b) for all layers."""
        self.trace = MLTrace()
        _zs, activations = self.net.forward(x)
        y = np.asarray(y_target, dtype=float)

        grad_W: list[np.ndarray] = [np.zeros_like(w) for w in self.net.weights]
        grad_b: list[np.ndarray] = [np.zeros_like(b) for b in self.net.biases]

        # Output layer error: delta = (a_L - y) * sigmoid'(z_L)
        a_L = activations[-1]
        loss = float(0.5 * np.sum((a_L - y) ** 2))
        delta = (a_L - y) * self.sigmoid_derivative(a_L)

        self.trace.record(
            name="output_error",
            description=f"Output loss={loss:.4f}, delta_L={delta.tolist()}",
            loss=loss,
            delta=delta.tolist(),
        )

        num_weight_layers = len(self.net.weights)
        curr_delta = delta

        for l_rev in range(num_weight_layers - 1, -1, -1):
            a_prev = activations[l_rev]
            grad_W[l_rev] = np.outer(curr_delta, a_prev)
            grad_b[l_rev] = curr_delta.copy()

            self.trace.record(
                name=f"grad_layer_{l_rev + 1}",
                description=(
                    f"Layer {l_rev + 1}: grad_W_norm={np.linalg.norm(grad_W[l_rev]):.4f}, "
                    f"grad_b_norm={np.linalg.norm(grad_b[l_rev]):.4f}"
                ),
                layer=l_rev + 1,
                grad_W_norm=float(np.linalg.norm(grad_W[l_rev])),
                grad_b_norm=float(np.linalg.norm(grad_b[l_rev])),
            )

            # Propagate delta to previous layer (if not input layer)
            if l_rev > 0:
                w_curr = self.net.weights[l_rev]
                a_prev_layer = activations[l_rev]
                curr_delta = np.dot(w_curr.T, curr_delta) * self.sigmoid_derivative(a_prev_layer)

        return grad_W, grad_b

    def finite_difference_check(
        self,
        x: Sequence[float] | np.ndarray,
        y_target: Sequence[float] | np.ndarray,
        epsilon: float = 1e-5,
    ) -> float:
        """Verify analytical gradients against finite differences; returns relative error."""
        grad_W_ana, _ = self.backward(x, y_target)
        y = np.asarray(y_target, dtype=float)

        ana_vector: list[float] = []
        num_vector: list[float] = []

        for l_idx, w_mat in enumerate(self.net.weights):
            for i in range(w_mat.shape[0]):
                for j in range(w_mat.shape[1]):
                    # Plus epsilon
                    w_mat[i, j] += epsilon
                    _, a_plus = self.net.forward(x)
                    loss_plus = 0.5 * np.sum((a_plus[-1] - y) ** 2)

                    # Minus epsilon
                    w_mat[i, j] -= 2 * epsilon
                    _, a_minus = self.net.forward(x)
                    loss_minus = 0.5 * np.sum((a_minus[-1] - y) ** 2)

                    # Reset weight
                    w_mat[i, j] += epsilon

                    num_grad = (loss_plus - loss_minus) / (2.0 * epsilon)
                    ana_grad = grad_W_ana[l_idx][i, j]

                    num_vector.append(num_grad)
                    ana_vector.append(ana_grad)

        vec_num = np.array(num_vector)
        vec_ana = np.array(ana_vector)
        diff_norm = np.linalg.norm(vec_ana - vec_num)
        denom = np.linalg.norm(vec_ana) + np.linalg.norm(vec_num)

        relative_error = float(diff_norm / (denom if denom > 1e-9 else 1.0))
        return relative_error


class BackpropagationVisualizer(MLComponent):
    """Component visualizer for forward pass and reverse gradient propagation wave."""

    def __init__(
        self,
        net: NeuralNetworkModel,
        input_data: Sequence[float] | np.ndarray,
        target_data: Sequence[float] | np.ndarray,
        *,
        layer_spacing: float = 2.4,
        node_spacing: float = 1.1,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.net = net
        self.input_data = np.asarray(input_data, dtype=float)
        self.target_data = np.asarray(target_data, dtype=float)
        self.layer_spacing = float(layer_spacing)
        self.node_spacing = float(node_spacing)

        self.model = BackpropagationModel(self.net)
        self.grad_W, self.grad_b = self.model.backward(self.input_data, self.target_data)
        self.zs, self.activations = self.net.forward(self.input_data)

        # Node coordinates
        self.node_positions: list[list[np.ndarray]] = []
        total_layers = len(self.net.layer_sizes)
        for l_idx, count in enumerate(self.net.layer_sizes):
            x = (l_idx - (total_layers - 1) / 2.0) * self.layer_spacing
            layer_pts = []
            for n_idx in range(count):
                y = ((count - 1) / 2.0 - n_idx) * self.node_spacing
                layer_pts.append(np.array([x, y, 0.0]))
            self.node_positions.append(layer_pts)

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        active_theme = get_active_theme()
        group = manim.VGroup()

        # Connections
        for l_idx in range(len(self.net.layer_sizes) - 1):
            curr_pts = self.node_positions[l_idx]
            next_pts = self.node_positions[l_idx + 1]
            for p1 in curr_pts:
                for p2 in next_pts:
                    line = manim.Line(p1, p2, color=active_theme.colors.border, stroke_width=1.2)
                    group.add(line)

        # Nodes
        for pts in self.node_positions:
            for p in pts:
                dot = manim.Dot(p, radius=0.22, color=active_theme.colors.surface)
                outline = manim.Circle(
                    radius=0.22, color=active_theme.colors.primary, stroke_width=2.0
                )
                outline.move_to(p)
                group.add(dot, outline)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for forward pass followed by backward backprop wave."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Base network structure
        base_group = manim.VGroup()
        weight_lines: list[list[manim.Line]] = []

        for l_idx in range(len(self.net.layer_sizes) - 1):
            layer_lines = []
            for p1 in self.node_positions[l_idx]:
                for p2 in self.node_positions[l_idx + 1]:
                    ln = manim.Line(p1, p2, color=active_theme.colors.border, stroke_width=1.2)
                    layer_lines.append(ln)
                    base_group.add(ln)
            weight_lines.append(layer_lines)

        node_circles: list[list[manim.Circle]] = []
        for pts in self.node_positions:
            l_circles = []
            for p in pts:
                dot = manim.Dot(p, radius=0.22, color=active_theme.colors.surface)
                outline = manim.Circle(
                    radius=0.22, color=active_theme.colors.primary, stroke_width=2.0
                )
                outline.move_to(p)
                base_group.add(dot, outline)
                l_circles.append(outline)
            node_circles.append(l_circles)

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(base_group),
                run_time=0.8,
                name="create_network_architecture",
            )
        )

        # 2. Forward pass glow
        for l_idx in range(len(self.net.layer_sizes)):
            node_glows = [
                c.animate.set_stroke(color=active_theme.colors.primary, width=3.5)
                for c in node_circles[l_idx]
            ]
            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.AnimationGroup(*node_glows),
                    run_time=0.3,
                    name=f"forward_layer_{l_idx}",
                )
            )

        # 3. Backward gradient wave
        for l_rev in range(len(self.net.layer_sizes) - 1, -1, -1):
            back_glows = [
                c.animate.set_stroke(color=active_theme.colors.accent, width=4.0)
                for c in node_circles[l_rev]
            ]
            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.AnimationGroup(*back_glows),
                    run_time=0.35,
                    name=f"backward_layer_{l_rev}",
                )
            )

            if l_rev > 0:
                synapse_back = [
                    ln.animate.set_stroke(color=active_theme.colors.accent, width=3.0)
                    for ln in weight_lines[l_rev - 1]
                ]
                animations.append(
                    Animation(
                        component=self,
                        manim_animation=manim.AnimationGroup(*synapse_back),
                        run_time=0.3,
                        name=f"backprop_synapses_{l_rev - 1}",
                    )
                )

        return animations


def backpropagation(
    net: NeuralNetworkModel,
    input_data: Sequence[float] | np.ndarray,
    target_data: Sequence[float] | np.ndarray,
) -> list[Animation]:
    """One-call functional API to animate backpropagation gradient flow."""
    viz = BackpropagationVisualizer(net, input_data, target_data)
    return viz.animate()


__all__ = [
    "BackpropagationModel",
    "BackpropagationVisualizer",
    "backpropagation",
]
