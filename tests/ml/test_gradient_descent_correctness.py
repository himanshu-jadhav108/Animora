"""Computational correctness tests for GradientDescentModel."""

from __future__ import annotations

import numpy as np

from animora.ml.optimization.gradient_descent import GradientDescentModel


def test_gradient_descent_quadratic_convergence() -> None:
    """Verify gradient descent converges to global minimum (0, 0) of f(x, y) = x^2 + y^2."""

    def loss_fn(x: float, y: float) -> float:
        return (x**2) + (y**2)

    model = GradientDescentModel(
        loss_fn=loss_fn,
        start=(3.0, 4.0),
        learning_rate=0.1,
        steps=50,
    )
    trajectory = model.optimize()

    assert len(trajectory) == 51
    # Check that initial loss is 25.0
    assert np.isclose(trajectory[0][2], 25.0)

    # Check strictly monotonically decreasing loss
    losses = [pt[2] for pt in trajectory]
    for k in range(len(losses) - 1):
        assert losses[k + 1] <= losses[k] + 1e-6

    # Check final point is near global minimum (0, 0)
    final_x, final_y, final_loss = trajectory[-1]
    assert np.isclose(final_x, 0.0, atol=1e-2)
    assert np.isclose(final_y, 0.0, atol=1e-2)
    assert np.isclose(final_loss, 0.0, atol=1e-3)


def test_gradient_descent_analytical_gradient() -> None:
    """Verify optimization with custom analytical gradient function."""

    def loss_fn(x: float, y: float) -> float:
        return 2 * (x**2) + 3 * (y**2)

    def grad_fn(x: float, y: float) -> tuple[float, float]:
        return 4 * x, 6 * y

    model = GradientDescentModel(
        loss_fn=loss_fn,
        start=(2.0, 1.0),
        learning_rate=0.08,
        steps=30,
        grad_fn=grad_fn,
    )
    trajectory = model.optimize()

    final_x, final_y, final_loss = trajectory[-1]
    assert np.isclose(final_x, 0.0, atol=1e-2)
    assert np.isclose(final_y, 0.0, atol=1e-2)
    assert np.isclose(final_loss, 0.0, atol=1e-3)
