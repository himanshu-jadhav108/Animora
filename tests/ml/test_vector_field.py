"""Unit tests for VectorField component."""

from __future__ import annotations

from animora.ml.vector_field import VectorField


def test_vector_field_sampling() -> None:
    def sample_grad(x: float, y: float) -> tuple[float, float]:
        return -2 * x, -2 * y

    vf = VectorField(sample_grad, x_range=(-2, 2, 1), y_range=(-2, 2, 1), step=1.0)
    samples = vf.sample_vectors()
    assert len(samples) == 25  # 5 xs (-2, -1, 0, 1, 2) * 5 ys

    # Check center vector
    center_sample = next(s for s in samples if abs(s[0]) < 1e-5 and abs(s[1]) < 1e-5)
    assert center_sample[2] == 0.0
    assert center_sample[3] == 0.0


def test_vector_field_animation() -> None:
    def simple_vec(x: float, y: float) -> tuple[float, float]:
        return 1.0, 1.0

    vf = VectorField(simple_vec, step=1.5)
    anim = vf.animate_create(run_time=0.6)
    assert anim.name == "create_vector_field"
    assert anim.run_time == 0.6
