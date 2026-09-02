"""Correctness tests for Tokenization model and visualizer."""

from __future__ import annotations

from animora.core.animation import Animation
from animora.ml.nlp.tokenization import (
    TokenizerModel,
    TokenizerVisualizer,
    tokenize,
)


def test_tokenization_exact_match() -> None:
    """Verify extracted token boundaries exactly match expected token list."""
    text = "The quick, brown fox jumps!"
    model = TokenizerModel(text)

    expected_tokens = ["The", "quick", ",", "brown", "fox", "jumps", "!"]
    assert model.tokens == expected_tokens
    assert len(model.spans) == len(expected_tokens)

    # Verify character spans reconstruct original substrings exactly
    for tok, (start, end) in zip(model.tokens, model.spans, strict=False):
        assert text[start:end] == tok

    assert len(model.trace) == 1
    assert model.trace[0].name == "tokenization"


def test_tokenization_one_call_api() -> None:
    anims = tokenize("Hello world!")
    assert len(anims) == 2
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "display_raw_text"


def test_tokenization_visualizer() -> None:
    viz = TokenizerVisualizer("Cat sat.")
    assert viz.n_tokens == 3
    assert len(viz.chip_positions) == 3
