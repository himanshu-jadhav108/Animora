"""Correctness tests for Word Embeddings and PCA projection reuse."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.classic.pca import PCAModel
from animora.ml.nlp.embeddings import (
    EmbeddingModel,
    EmbeddingVisualizer,
    word_embeddings,
)


def test_embeddings_pca_reuse_correctness() -> None:
    """Verify EmbeddingModel projects D-dimensional embeddings using Phase 13b PCAModel."""
    tokens = ["king", "queen", "man", "woman", "apple"]
    model = EmbeddingModel(tokens, embed_dim=4, random_seed=42)

    assert model.embeddings.shape == (5, 4)
    assert model.projected_2d.shape == (5, 2)
    assert model.pca_model is not None

    # Independent reference computation reusing PCAModel directly
    ref_pca = PCAModel(model.embeddings, n_components=2)
    expected_projected = np.dot(ref_pca.X_centered, ref_pca.components[:2].T)

    assert np.allclose(model.projected_2d, expected_projected, atol=1e-7)
    assert len(model.trace) == 1


def test_embeddings_one_call_api() -> None:
    anims = word_embeddings(["cat", "dog", "fish"], embed_dim=4)
    assert len(anims) == 2
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "create_embedding_axes"


def test_embeddings_visualizer() -> None:
    viz = EmbeddingVisualizer(["a", "b", "c"], embed_dim=3)
    assert viz.axes is not None
    assert len(viz.model.tokens) == 3
