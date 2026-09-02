"""Computational and trace correctness tests for Linear Regression."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.linear_regression import (
    LinearRegressionModel,
    LinearRegressionVisualizer,
    linear_regression,
)


def test_linear_regression_correctness_vs_polyfit() -> None:
    """Verify LinearRegressionModel matches numpy.polyfit ground truth."""
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.1, 4.2, 5.9, 8.1, 9.9])

    # Reference computation via numpy.polyfit
    ref_w, ref_b = np.polyfit(x, y, deg=1)

    model = LinearRegressionModel(x, y)
    assert np.isclose(model.optimal_w, ref_w, atol=1e-5)
    assert np.isclose(model.optimal_b, ref_b, atol=1e-5)


def test_linear_regression_gradient_descent_trace() -> None:
    """Verify gradient descent fitting records iteration steps and converges."""
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    y = 2.5 * x + 1.0

    model = LinearRegressionModel(x, y, learning_rate=0.1, steps=20)
    traj = model.fit_gradient_descent()

    assert len(traj) >= 20
    assert len(model.trace) == 21
    # Check that final parameters are close to true slope 2.5 and intercept 1.0
    final_w, final_b, final_mse = traj[-1]
    assert np.isclose(final_w, 2.5, atol=0.05)
    assert np.isclose(final_b, 1.0, atol=0.2)
    assert final_mse < 0.1


def test_linear_regression_one_call_api() -> None:
    x = [0.0, 1.0, 2.0, 3.0]
    y = [1.0, 3.0, 5.0, 7.0]
    anims = linear_regression(x, y, steps=5)

    assert len(anims) >= 5
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_data_and_axes"


def test_linear_regression_visualizer() -> None:
    x = [1.0, 2.0, 3.0]
    y = [2.0, 4.0, 6.0]
    viz = LinearRegressionVisualizer(x, y, steps=4)
    assert viz.axes is not None
    assert len(viz.trajectory) == 6
