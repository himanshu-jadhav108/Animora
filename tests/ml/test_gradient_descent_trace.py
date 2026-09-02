"""Trace and animation sequence tests for gradient descent."""

from __future__ import annotations

from animora.core.animation import Animation
from animora.ml.optimization.gradient_descent import (
    GradientDescentVisualizer,
    gradient_descent,
)


def test_gradient_descent_trace_step_alignment() -> None:
    def loss_fn(x: float, y: float) -> float:
        return (x**2) + (y**2)

    viz = GradientDescentVisualizer(loss_fn, start=(2.0, 2.0), steps=10)
    anims = viz.animate()

    # 1 surface create + 10 step movement animations
    assert len(anims) == 11
    assert anims[0].name == "create_surface_plot"
    for idx, anim in enumerate(anims[1:]):
        assert anim.name == f"gd_step_{idx}"
        assert isinstance(anim, Animation)


def test_gradient_descent_one_call_api() -> None:
    def loss_fn(x: float, y: float) -> float:
        return (x**2) + (y**2)

    anims = gradient_descent(loss_fn, start=(1.5, 1.5), steps=8)
    assert len(anims) == 9
    assert all(isinstance(a, Animation) for a in anims)
