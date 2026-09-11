"""Neural Network Explainer scene template for deep learning architectures."""

from __future__ import annotations

from typing import Any

from animora.ml.deep_learning.neural_network import NeuralNetworkVisualizer
from animora.templates.base import BaseTemplateScene


class NeuralNetworkExplainerTemplate(BaseTemplateScene):
    """Template for illustrating neural network architectures and forward propagation.

    When to use this:
        Use this template when explaining multilayer perceptrons, deep learning layer
        dimensions, activation function transformations, and signal flow through
        dense representations.

    Layout Architecture:
        - Top: Header & Layer Architecture Specification
        - Center: Layered feedforward neural network visualization
        - Bottom: Tensor dimension and forward pass narrative
    """

    def __init__(
        self,
        title: str = "Feedforward Neural Network Architecture",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.nn_title = title

    def construct_template(self) -> None:
        # 1. Header & Narration
        self.setup_header(self.nn_title)
        self.setup_footer_narrator(
            "Constructing dense architecture: Input(2) -> Hidden(3) -> Output(1)..."
        )

        # 2. Centered Neural Network
        nn_viz = NeuralNetworkVisualizer(
            layer_sizes=[2, 3, 1],
            input_data=[0.5, -0.2],
            layer_spacing=2.2,
            node_spacing=0.9,
        )
        nn_viz.move_to([0.0, 0.0, 0.0])
        self.play(nn_viz.animate_create(run_time=0.8))

        # 3. Forward flow
        self.narrate("Propagating input vector through hidden layer activations...")
        for anim in nn_viz.animate():
            self.play(anim)
        self.wait(0.5)


__all__ = [
    "NeuralNetworkExplainerTemplate",
]
