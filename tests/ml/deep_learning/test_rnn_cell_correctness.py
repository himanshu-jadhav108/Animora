"""Correctness tests for RNN cell sequential state update."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.deep_learning.rnn_cell import (
    RNNCellModel,
    RNNVisualizer,
    rnn_forward,
)


def test_rnn_cell_forward_vs_reference() -> None:
    """Verify RNN recurrence states strictly match independent NumPy loop."""
    rng = np.random.default_rng(42)
    w_xh = rng.normal(size=(2, 3))
    w_hh = rng.normal(size=(2, 2))
    b_h = np.array([0.1, -0.1])

    model = RNNCellModel(
        input_dim=3,
        hidden_dim=2,
        W_xh=w_xh,
        W_hh=w_hh,
        b_h=b_h,
    )

    X = np.array(
        [
            [0.5, -0.2, 0.1],
            [0.2, 0.4, -0.5],
            [-0.1, 0.3, 0.8],
        ]
    )

    states = model.forward_sequence(X)

    # Independent reference loop
    h_curr = np.zeros(2)
    ref_states = [h_curr.copy()]
    for t in range(len(X)):
        h_curr = np.tanh(np.dot(w_xh, X[t]) + np.dot(w_hh, h_curr) + b_h)
        ref_states.append(h_curr.copy())

    assert len(states) == len(ref_states)
    for s_act, s_exp in zip(states, ref_states, strict=False):
        assert np.allclose(s_act, s_exp, atol=1e-7)

    assert len(model.trace) == 3


def test_rnn_one_call_api() -> None:
    X = [[1.0, 0.0], [0.0, 1.0]]
    anims = rnn_forward(X, hidden_dim=2)

    assert len(anims) == 2
    assert all(isinstance(a, Animation) for a in anims)
    assert anims[0].name == "unroll_step_0"


def test_rnn_visualizer() -> None:
    X = [[0.5, 0.5]]
    viz = RNNVisualizer(X, hidden_dim=2)
    assert len(viz.cell_centers) == 1
    assert len(viz.hidden_states) == 2
