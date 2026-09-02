"""Correctness tests for minimal Transformer Block composition."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.nlp.transformer_block import (
    TransformerBlockModel,
    TransformerBlockVisualizer,
    transformer_block,
)


def test_transformer_block_composition_matches_reference() -> None:
    """Verify transformer block output matches independent attention + feedforward."""
    X = np.array(
        [
            [1.0, -0.5, 0.2],
            [0.3, 0.8, -0.1],
        ]
    )
    model = TransformerBlockModel(X, d_k=2, d_ff=3, random_seed=42)

    # Reference independent feed-forward
    attn_out = model.attn_output
    hidden_ref = np.maximum(0.0, np.dot(attn_out, model.W1) + model.b1)
    ffn_ref = np.dot(hidden_ref, model.W2) + model.b2

    assert np.allclose(model.ffn_output, ffn_ref, atol=1e-7)
    assert model.ffn_output.shape == X.shape
    assert len(model.trace) == 1


def test_transformer_block_one_call_api() -> None:
    X = [[1.0, 0.0], [0.0, 1.0]]
    anims = transformer_block(X, d_k=2, d_ff=3)
    assert len(anims) == 2
    assert all(isinstance(a, Animation) for a in anims)


def test_transformer_block_visualizer() -> None:
    X = [[0.5, 0.5]]
    viz = TransformerBlockVisualizer(X, d_k=2, d_ff=2)
    assert viz.attn_card is not None
    assert viz.ffn_card is not None
