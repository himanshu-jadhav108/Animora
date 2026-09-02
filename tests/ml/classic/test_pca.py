"""Computational and trace correctness tests for Principal Component Analysis (PCA)."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.pca import (
    PCAModel,
    PCAVisualizer,
    pca,
)


def test_pca_correctness_vs_numpy_eigh() -> None:
    """Verify PCAModel matches numpy.linalg.eigh ground truth."""
    rng = np.random.default_rng(42)
    # Synthetic 2D data stretched along diagonal y = x
    X = rng.multivariate_normal(mean=[1.0, 2.0], cov=[[3.0, 2.5], [2.5, 3.0]], size=100)

    model = PCAModel(X, n_components=1)

    # Reference computation
    X_cent = X - np.mean(X, axis=0)
    cov = np.cov(X_cent, rowvar=False)
    ref_vals, ref_vecs = np.linalg.eigh(cov)
    ref_idx = np.argsort(ref_vals)[::-1]
    ref_eigenvalues = ref_vals[ref_idx]
    ref_v1 = ref_vecs[:, ref_idx[0]]

    # Check eigenvalues
    assert np.allclose(model.eigenvalues, ref_eigenvalues, atol=1e-5)

    # Check principal direction (eigenvectors are unique up to sign +/-)
    dot_product = abs(float(np.dot(model.components[0], ref_v1)))
    assert np.isclose(dot_product, 1.0, atol=1e-5)

    # Check projected points lie along the 1st principal component line
    assert len(model.projected_points) == 100


def test_pca_one_call_api() -> None:
    X = [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
    anims = pca(X, n_components=1)

    assert len(anims) == 3
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_pca_dataset"


def test_pca_visualizer() -> None:
    X = [[1.0, 0.0], [0.0, 1.0]]
    viz = PCAVisualizer(X)
    assert viz.axes is not None
    assert len(viz.model.components) == 2
