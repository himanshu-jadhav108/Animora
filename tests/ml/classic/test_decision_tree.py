"""Computational and trace correctness tests for Decision Tree."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.decision_tree import (
    DecisionTreeModel,
    DecisionTreeVisualizer,
    decision_tree,
)


def test_decision_tree_gini_calculation() -> None:
    """Verify Gini impurity computation."""
    model = DecisionTreeModel([[0.0]], [0])

    # Pure labels -> Gini = 0.0
    pure_labels = np.array([0, 0, 0, 0])
    assert np.isclose(model._compute_impurity(pure_labels), 0.0)

    # 50/50 binary split -> Gini = 1 - (0.5^2 + 0.5^2) = 0.5
    half_labels = np.array([0, 0, 1, 1])
    assert np.isclose(model._compute_impurity(half_labels), 0.5)


def test_decision_tree_split_selection() -> None:
    """Verify best split finds optimal threshold on 1D feature."""
    # Data clearly separated at X = 2.5
    X = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([0, 0, 1, 1])

    model = DecisionTreeModel(X, y, max_depth=1)
    root = model.fit()

    assert not root.is_leaf
    assert root.feature_idx == 0
    assert np.isclose(root.threshold or 0.0, 2.5)
    assert root.left is not None and root.left.is_leaf
    assert root.right is not None and root.right.is_leaf
    assert root.left.prediction == 0
    assert root.right.prediction == 1


def test_decision_tree_one_call_api() -> None:
    X = [[1.0, 2.0], [1.5, 1.8], [5.0, 6.0], [5.5, 6.2]]
    y = [0, 0, 1, 1]

    anims = decision_tree(X, y, max_depth=2)
    assert len(anims) >= 2
    assert all(isinstance(a, Animation) for a in anims)


def test_decision_tree_visualizer_uses_tree_layout() -> None:
    X = [[1.0], [2.0], [5.0], [6.0]]
    y = [0, 0, 1, 1]

    viz = DecisionTreeVisualizer(X, y, max_depth=1)
    assert len(viz.edges) >= 1
    assert viz.root.node_id in viz.nodes_map
