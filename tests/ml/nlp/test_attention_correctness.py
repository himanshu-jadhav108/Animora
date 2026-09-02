"""Correctness tests for Scaled Dot-Product Attention, including softmax-sums-to-1 verification."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.nlp.attention import (
    AttentionModel,
    AttentionVisualizer,
    attention,
)


def test_attention_softmax_rows_sum_to_one() -> None:
    """Mandatory verification: every row of attention_weights matrix sums to 1.0."""
    X = np.array(
        [
            [1.0, 0.5, -0.2],
            [0.1, 0.9, 0.3],
            [-0.4, 0.2, 0.7],
            [0.8, -0.1, 0.5],
        ]
    )
    model = AttentionModel(X, d_k=3, random_seed=42)

    row_sums = np.sum(model.attention_weights, axis=-1)
    expected_ones = np.ones(model.seq_len)

    # Mandatory numerical check
    assert np.allclose(row_sums, expected_ones, atol=1e-6), (
        f"Softmax rows do not sum to 1.0: {row_sums}"
    )
    assert np.all(model.attention_weights >= 0.0)


def test_attention_independent_reference_computation() -> None:
    """Verify Q, K, V, scores, weights, and output match independent manual NumPy calculation."""
    X = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )
    W_q = np.array([[1.0, 0.0], [0.0, 1.0]])
    W_k = np.array([[0.5, 0.5], [-0.5, 0.5]])
    W_v = np.array([[2.0, 1.0], [1.0, 2.0]])

    model = AttentionModel(X, d_k=2, W_q=W_q, W_k=W_k, W_v=W_v)

    # Independent reference
    ref_Q = np.dot(X, W_q)
    ref_K = np.dot(X, W_k)
    ref_V = np.dot(X, W_v)

    ref_scores = np.dot(ref_Q, ref_K.T) / np.sqrt(2.0)
    ref_exp = np.exp(ref_scores - np.max(ref_scores, axis=-1, keepdims=True))
    ref_weights = ref_exp / np.sum(ref_exp, axis=-1, keepdims=True)
    ref_output = np.dot(ref_weights, ref_V)

    assert np.allclose(model.Q, ref_Q, atol=1e-7)
    assert np.allclose(model.K, ref_K, atol=1e-7)
    assert np.allclose(model.V, ref_V, atol=1e-7)
    assert np.allclose(model.scores, ref_scores, atol=1e-7)
    assert np.allclose(model.attention_weights, ref_weights, atol=1e-7)
    assert np.allclose(model.output, ref_output, atol=1e-7)


def test_attention_one_call_api() -> None:
    X = [[1.0, 0.0], [0.0, 1.0]]
    anims = attention(X, d_k=2)
    assert len(anims) == 2
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "show_attention_weights"


def test_attention_visualizer() -> None:
    X = [[1.0, 0.5], [0.2, 0.8]]
    viz = AttentionVisualizer(X, d_k=2)
    assert viz.weights_grid is not None
    assert viz.output_grid is not None
