"""Computational and trace correctness tests for K-Means clustering."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.kmeans import (
    KMeansModel,
    KMeansVisualizer,
    kmeans,
)


def test_kmeans_correctness() -> None:
    """Verify K-Means convergence on two widely separated clusters."""
    cluster1 = np.array([[-5.0, -5.0], [-4.8, -5.2], [-5.2, -4.9]])
    cluster2 = np.array([[5.0, 5.0], [4.9, 5.1], [5.1, 4.8]])
    data = np.vstack([cluster1, cluster2])

    init_centroids = np.array([[-4.0, -4.0], [4.0, 4.0]])
    model = KMeansModel(data, k=2, max_iters=10, initial_centroids=init_centroids)
    history = model.fit()

    assert len(history) >= 1
    final_entry = history[-1]
    final_centroids = final_entry["centroids"]
    assignments = final_entry["assignments"]

    # Cluster 1 samples should have same label, Cluster 2 samples should have different label
    assert len(np.unique(assignments[:3])) == 1
    assert len(np.unique(assignments[3:])) == 1
    assert assignments[0] != assignments[3]

    # Verify centroids match true cluster centers (-5, -5) and (5, 5)
    c1_mean = np.mean(cluster1, axis=0)
    c2_mean = np.mean(cluster2, axis=0)

    dists_to_c1 = [np.linalg.norm(c - c1_mean) for c in final_centroids]
    dists_to_c2 = [np.linalg.norm(c - c2_mean) for c in final_centroids]
    assert min(dists_to_c1) < 0.1
    assert min(dists_to_c2) < 0.1


def test_kmeans_trace_recording() -> None:
    data = np.array([[0.0, 0.0], [0.1, 0.2], [5.0, 5.0], [5.2, 5.1]])
    model = KMeansModel(data, k=2, max_iters=5, random_state=1)
    history = model.fit()

    assert len(model.trace) == len(history)
    assert model.trace[0].name == "iteration"
    assert "inertia" in model.trace[0].values


def test_kmeans_one_call_api() -> None:
    data = [[-1.0, -1.0], [1.0, 1.0], [2.0, 2.0], [-2.0, -2.0]]
    anims = kmeans(data, k=2, max_iters=3)

    assert len(anims) >= 2
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_kmeans_data"


def test_kmeans_visualizer() -> None:
    data = [[0.0, 0.0], [1.0, 1.0]]
    viz = KMeansVisualizer(data, k=2, max_iters=2)
    assert viz.axes is not None
    assert len(viz.history) >= 1
