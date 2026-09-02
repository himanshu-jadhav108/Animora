"""Correctness tests for CNN 2D convolution operation."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.deep_learning.cnn_convolution import (
    CNNConvolutionModel,
    CNNConvolutionVisualizer,
    cnn_convolution,
)


def test_cnn_convolution_known_hand_calculated_matrix() -> None:
    """Verify CNN 2D convolution output against known hand-calculated arithmetic."""
    image = np.array(
        [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
        ]
    )
    kernel = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ]
    )

    model = CNNConvolutionModel(image, kernel, stride=1)
    steps = model.compute()

    expected_output = np.array(
        [
            [6.0, 8.0],
            [12.0, 14.0],
        ]
    )

    assert np.allclose(model.output, expected_output, atol=1e-6)
    assert len(steps) == 4
    assert len(model.trace) == 4
    assert np.isclose(steps[0]["val"], 6.0)
    assert np.isclose(steps[3]["val"], 14.0)


def test_cnn_convolution_stride_2() -> None:
    image = np.ones((4, 4))
    kernel = np.ones((2, 2))
    model = CNNConvolutionModel(image, kernel, stride=2)
    model.compute()

    assert model.output.shape == (2, 2)
    assert np.allclose(model.output, 4.0)


def test_cnn_convolution_one_call_api() -> None:
    image = [[1.0, 2.0], [3.0, 4.0]]
    kernel = [[1.0]]
    anims = cnn_convolution(image, kernel)

    assert len(anims) >= 2
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_conv_grids"


def test_cnn_convolution_visualizer() -> None:
    image = [[1.0, 2.0], [3.0, 4.0]]
    kernel = [[1.0, 0.0], [0.0, 1.0]]
    viz = CNNConvolutionVisualizer(image, kernel)
    assert viz.input_grid is not None
    assert viz.output_grid is not None
