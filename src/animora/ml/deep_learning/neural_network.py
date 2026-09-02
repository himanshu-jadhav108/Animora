"""Feedforward neural network structure, forward pass model, and one-call visualizer."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class NeuralNetworkModel:
    """Mathematical multi-layer perceptron running real matrix multiplications and activations."""

    def __init__(
        self,
        layer_sizes: Sequence[int],
        *,
        weights: Sequence[np.ndarray] | None = None,
        biases: Sequence[np.ndarray] | None = None,
        activation: str = "sigmoid",
        random_seed: int = 42,
    ) -> None:
        self.layer_sizes = [int(s) for s in layer_sizes]
        if len(self.layer_sizes) < 2:
            raise ValueError("layer_sizes must contain at least 2 layers (input and output).")

        self.activation_name = activation.lower()
        self.trace = MLTrace()

        rng = np.random.default_rng(random_seed)
        self.weights: list[np.ndarray] = []
        self.biases: list[np.ndarray] = []

        for i in range(len(self.layer_sizes) - 1):
            n_in, n_out = self.layer_sizes[i], self.layer_sizes[i + 1]
            if weights is not None and i < len(weights):
                w = np.asarray(weights[i], dtype=float)
            else:
                # Xavier initialization
                w = rng.normal(0.0, np.sqrt(2.0 / (n_in + n_out)), size=(n_out, n_in))
            self.weights.append(w)

            if biases is not None and i < len(biases):
                b = np.asarray(biases[i], dtype=float)
            else:
                b = np.zeros(n_out, dtype=float)
            self.biases.append(b)

    def activate(self, z: np.ndarray) -> np.ndarray:
        """Apply non-linear activation function."""
        if self.activation_name == "relu":
            return np.asarray(np.maximum(0.0, z), dtype=float)
        elif self.activation_name == "tanh":
            return np.asarray(np.tanh(z), dtype=float)
        elif self.activation_name == "linear":
            return np.asarray(z, dtype=float)
        # Default sigmoid
        return np.asarray(
            np.where(z >= 0, 1.0 / (1.0 + np.exp(-z)), np.exp(z) / (1.0 + np.exp(z))),
            dtype=float,
        )

    def forward(self, x: Sequence[float] | np.ndarray) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """Compute full forward pass returning all layer pre-activations (z) and activations (a)."""
        self.trace = MLTrace()
        a_curr = np.asarray(x, dtype=float)
        if len(a_curr) != self.layer_sizes[0]:
            raise ValueError(f"Input dimension {len(a_curr)} does not match {self.layer_sizes[0]}.")

        zs: list[np.ndarray] = [a_curr.copy()]  # Input has no z, store x for alignment
        activations: list[np.ndarray] = [a_curr.copy()]

        self.trace.record(
            name="input_layer",
            description=f"Layer 0 (Input): a={a_curr.tolist()}",
            layer=0,
            activations=a_curr.tolist(),
        )

        for l_idx in range(len(self.weights)):
            w = self.weights[l_idx]
            b = self.biases[l_idx]
            z = np.dot(w, a_curr) + b
            zs.append(z)

            a_next = self.activate(z)
            activations.append(a_next)
            a_curr = a_next

            self.trace.record(
                name=f"layer_{l_idx + 1}",
                description=f"Layer {l_idx + 1}: z={z.tolist()}, a={a_next.tolist()}",
                layer=l_idx + 1,
                z=z.tolist(),
                activations=a_next.tolist(),
            )

        return zs, activations


class NeuralNetworkVisualizer(MLComponent):
    """Visualizes neural network architecture, synaptic weights, and forward activation flow."""

    def __init__(
        self,
        layer_sizes: Sequence[int],
        input_data: Sequence[float] | np.ndarray,
        *,
        weights: Sequence[np.ndarray] | None = None,
        biases: Sequence[np.ndarray] | None = None,
        activation: str = "sigmoid",
        layer_spacing: float = 2.4,
        node_spacing: float = 1.1,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.layer_sizes = [int(s) for s in layer_sizes]
        self.input_data = np.asarray(input_data, dtype=float)
        self.layer_spacing = float(layer_spacing)
        self.node_spacing = float(node_spacing)

        self.model = NeuralNetworkModel(
            self.layer_sizes,
            weights=weights,
            biases=biases,
            activation=activation,
        )
        self.zs, self.activations = self.model.forward(self.input_data)

        # Precompute 3D node coordinates
        self.node_positions: list[list[np.ndarray]] = []
        total_layers = len(self.layer_sizes)
        for l_idx, count in enumerate(self.layer_sizes):
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
        for l_idx in range(len(self.layer_sizes) - 1):
            curr_pts = self.node_positions[l_idx]
            next_pts = self.node_positions[l_idx + 1]
            for p1 in curr_pts:
                for p2 in next_pts:
                    line = manim.Line(p1, p2, color=active_theme.colors.border, stroke_width=1.2)
                    group.add(line)

        # Nodes
        for l_idx, pts in enumerate(self.node_positions):
            for n_idx, p in enumerate(pts):
                val = float(self.activations[l_idx][n_idx])
                dot = manim.Dot(p, radius=0.22, color=active_theme.colors.surface)
                outline = manim.Circle(
                    radius=0.22, color=active_theme.colors.primary, stroke_width=2.0
                )
                outline.move_to(p)
                txt = manim.Text(f"{val:.2f}", font_size=12, color=active_theme.colors.text)
                txt.move_to(p)
                group.add(dot, outline, txt)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation visualizing network structure and layer-by-layer forward pass."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Spawn network structure
        base_group = manim.VGroup()
        weight_lines: list[list[manim.Line]] = []

        for l_idx in range(len(self.layer_sizes) - 1):
            layer_lines = []
            for p1 in self.node_positions[l_idx]:
                for p2 in self.node_positions[l_idx + 1]:
                    ln = manim.Line(p1, p2, color=active_theme.colors.border, stroke_width=1.2)
                    layer_lines.append(ln)
                    base_group.add(ln)
            weight_lines.append(layer_lines)

        node_circles: list[list[manim.Circle]] = []
        for _l_idx, pts in enumerate(self.node_positions):
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

        # 2. Layer-by-layer forward activation propagation
        for l_idx in range(len(self.layer_sizes)):
            node_glows = []
            for _n_idx, circ in enumerate(node_circles[l_idx]):
                glow = circ.animate.set_stroke(color=active_theme.colors.accent, width=3.5)
                node_glows.append(glow)

            animations.append(
                Animation(
                    component=self,
                    manim_animation=manim.AnimationGroup(*node_glows),
                    run_time=0.4,
                    name=f"activate_layer_{l_idx}",
                )
            )

            # Animate synaptic pulse to next layer
            if l_idx < len(self.layer_sizes) - 1:
                synapse_anims = [
                    ln.animate.set_stroke(color=active_theme.colors.primary, width=2.5)
                    for ln in weight_lines[l_idx]
                ]
                animations.append(
                    Animation(
                        component=self,
                        manim_animation=manim.AnimationGroup(*synapse_anims),
                        run_time=0.3,
                        name=f"propagate_synapses_{l_idx}",
                    )
                )

        return animations


def neural_network_forward(
    layer_sizes: Sequence[int],
    input_data: Sequence[float] | np.ndarray,
    *,
    weights: Sequence[np.ndarray] | None = None,
    biases: Sequence[np.ndarray] | None = None,
    activation: str = "sigmoid",
) -> list[Animation]:
    """One-call functional API to animate neural network forward pass."""
    viz = NeuralNetworkVisualizer(
        layer_sizes,
        input_data,
        weights=weights,
        biases=biases,
        activation=activation,
    )
    return viz.animate()


__all__ = [
    "NeuralNetworkModel",
    "NeuralNetworkVisualizer",
    "neural_network_forward",
]
