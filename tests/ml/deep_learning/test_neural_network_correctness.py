"""Correctness tests for Neural Network structure and forward pass."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.deep_learning.neural_network import (
    NeuralNetworkModel,
    NeuralNetworkVisualizer,
    neural_network_forward,
)


def test_forward_pass_vs_numpy_reference() -> None:
    """Verify computed activations strictly match raw NumPy matrix multiplications."""
    layer_sizes = [3, 4, 2]
    rng = np.random.default_rng(123)

    w1 = rng.normal(size=(4, 3))
    b1 = rng.normal(size=4)
    w2 = rng.normal(size=(2, 4))
    b2 = rng.normal(size=2)

    model = NeuralNetworkModel(
        layer_sizes,
        weights=[w1, w2],
        biases=[b1, b2],
        activation="sigmoid",
    )

    x = np.array([0.5, -0.2, 0.8])
    zs, activations = model.forward(x)

    # Reference independent computation
    z1_ref = np.dot(w1, x) + b1
    a1_ref = 1.0 / (1.0 + np.exp(-z1_ref))

    z2_ref = np.dot(w2, a1_ref) + b2
    a2_ref = 1.0 / (1.0 + np.exp(-z2_ref))

    assert np.allclose(zs[1], z1_ref, atol=1e-7)
    assert np.allclose(activations[1], a1_ref, atol=1e-7)
    assert np.allclose(zs[2], z2_ref, atol=1e-7)
    assert np.allclose(activations[2], a2_ref, atol=1e-7)


def test_neural_network_one_call_api() -> None:
    anims = neural_network_forward([2, 3, 1], [0.5, -0.5])
    assert len(anims) >= 3
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_network_architecture"


def test_neural_network_visualizer() -> None:
    viz = NeuralNetworkVisualizer([2, 2], [1.0, 1.0])
    assert len(viz.node_positions) == 2
    assert len(viz.activations) == 2
