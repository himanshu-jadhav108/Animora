"""Computational and trace correctness tests for Support Vector Machine (SVM)."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.svm import (
    HardMarginSVMModel,
    SVMVisualizer,
    svm,
)


def test_svm_correctness_and_support_vectors() -> None:
    """Verify linear SVM finds separating hyperplane and identifies support vectors."""
    # Linearly separable along x-axis with boundary near x=0
    X = np.array(
        [
            [-2.0, 0.0],
            [-1.0, 1.0],
            [-1.0, -1.0],
            [1.0, 1.0],
            [1.0, -1.0],
            [2.0, 0.0],
        ]
    )
    y = np.array([-1, -1, -1, 1, 1, 1])

    model = HardMarginSVMModel(X, y, learning_rate=0.05, max_iters=200)
    w, b, sv_indices = model.fit()

    # Separating normal vector should primarily align with x-axis
    # (w[0] > 0 and |w[0]| > |w[1]|)
    assert w[0] > 0
    assert abs(w[0]) > abs(w[1])

    # Check that predictions sign(w*x + b) are 100% accurate
    predictions = np.sign(np.dot(X, w) + b)
    assert np.all(predictions == y)

    # Support vectors should be the points closest to boundary (x=-1 and x=+1)
    assert len(sv_indices) >= 2


def test_svm_one_call_api() -> None:
    X = [[-1.0, 0.0], [1.0, 0.0]]
    y = [-1, 1]

    anims = svm(X, y)
    assert len(anims) == 3
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_svm_dataset"


def test_svm_visualizer() -> None:
    X = [[-2.0, 0.0], [2.0, 0.0]]
    y = [-1, 1]
    viz = SVMVisualizer(X, y)
    assert viz.axes is not None
    p1, p2 = viz._get_line_endpoints(0.0)
    assert len(p1) == 3
    assert len(p2) == 3
