"""Computational and trace correctness tests for Logistic Regression."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.logistic_regression import (
    LogisticRegressionModel,
    LogisticRegressionVisualizer,
    logistic_regression,
)


def test_logistic_regression_correctness() -> None:
    """Verify LogisticRegressionModel decreases loss on linearly separable data."""
    # Two distinct 2D clusters
    X = np.array(
        [
            [-2.0, -2.0],
            [-1.5, -1.0],
            [-2.5, -1.8],
            [2.0, 2.0],
            [1.5, 1.8],
            [2.5, 2.2],
        ]
    )
    y = np.array([0, 0, 0, 1, 1, 1])

    model = LogisticRegressionModel(X, y, learning_rate=0.5, steps=30)
    traj = model.fit()

    assert len(traj) == 31
    assert len(model.trace) == 31

    # Verify cross-entropy loss monotonically decreases overall
    initial_loss = traj[0][3]
    final_loss = traj[-1][3]
    assert final_loss < initial_loss
    assert final_loss < 0.25


def test_logistic_regression_one_call_api() -> None:
    X = [[-1.0, -1.0], [1.0, 1.0]]
    y = [0, 1]
    anims = logistic_regression(X, y, steps=5)

    assert len(anims) >= 5
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_classification_data"


def test_logistic_regression_visualizer() -> None:
    X = [[-1.0, 0.0], [1.0, 0.0]]
    y = [0, 1]
    viz = LogisticRegressionVisualizer(X, y, steps=3)
    assert viz.axes is not None
    p1, p2 = viz._get_boundary_endpoints(1.0, 0.0, 0.0)
    assert len(p1) == 3
    assert len(p2) == 3
