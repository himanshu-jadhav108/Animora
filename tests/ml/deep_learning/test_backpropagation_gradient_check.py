"""Mandatory finite-difference gradient check verifying analytical backpropagation."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.deep_learning.backpropagation import (
    BackpropagationModel,
    BackpropagationVisualizer,
    backpropagation,
)
from animora.ml.deep_learning.neural_network import NeuralNetworkModel


def test_backpropagation_finite_difference_check() -> None:
    """Rigorous gradient check comparing analytical gradients to numerical finite differences.

    The relative error norm must be strictly less than 1e-5.
    """
    layer_sizes = [2, 3, 1]
    net = NeuralNetworkModel(layer_sizes, activation="sigmoid", random_seed=42)

    model = BackpropagationModel(net)
    x = np.array([0.7, -0.4])
    y_target = np.array([1.0])

    relative_error = model.finite_difference_check(x, y_target, epsilon=1e-5)

    # Mandatory assertion: relative error must pass within strict numerical tolerance
    assert relative_error < 1e-5, f"Gradient check failed with relative error: {relative_error}"


def test_backpropagation_multi_output_gradient_check() -> None:
    """Verify gradient checking on multi-output architecture [3, 4, 2]."""
    layer_sizes = [3, 4, 2]
    net = NeuralNetworkModel(layer_sizes, activation="sigmoid", random_seed=99)

    model = BackpropagationModel(net)
    x = np.array([0.2, 0.5, -0.8])
    y_target = np.array([0.0, 1.0])

    relative_error = model.finite_difference_check(x, y_target, epsilon=1e-5)
    assert relative_error < 1e-5


def test_backpropagation_one_call_api() -> None:
    net = NeuralNetworkModel([2, 2, 1], activation="sigmoid")
    anims = backpropagation(net, [0.5, 0.5], [1.0])

    assert len(anims) >= 4
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_network_architecture"


def test_backpropagation_visualizer() -> None:
    net = NeuralNetworkModel([2, 2, 1], activation="sigmoid")
    viz = BackpropagationVisualizer(net, [0.1, 0.2], [0.8])
    assert len(viz.grad_W) == 2
    assert len(viz.grad_b) == 2
