"""Unit tests for SurfacePlot component."""

from __future__ import annotations

import numpy as np

from animora.ml.surface_plot import SurfacePlot


def test_surface_plot_grid_evaluation() -> None:
    def quadratic(x: float, y: float) -> float:
        return (x**2) + (y**2)

    surf = SurfacePlot(quadratic, x_range=(-2, 2, 1), y_range=(-2, 2, 1), resolution=15)
    X, Y, Z = surf.evaluate_grid()

    assert X.shape == (15, 15)
    assert Y.shape == (15, 15)
    assert Z.shape == (15, 15)
    assert np.isclose(Z[7, 7], 0.0, atol=0.1)


def test_surface_plot_coordinate_mapping() -> None:
    def plane(x: float, y: float) -> float:
        return x + y

    surf = SurfacePlot(plane, x_range=(-5, 5, 1), y_range=(-5, 5, 1))
    p = surf.c2p(0.0, 0.0)
    assert isinstance(p, np.ndarray)
    assert len(p) == 3

    data_xy = surf.p2c(p)
    assert np.isclose(data_xy[0], 0.0, atol=1e-5)
    assert np.isclose(data_xy[1], 0.0, atol=1e-5)


def test_surface_plot_animation() -> None:
    def loss(x: float, y: float) -> float:
        return x * y

    surf = SurfacePlot(loss)
    anim = surf.animate_create(run_time=0.8)
    assert anim.name == "create_surface_plot"
    assert anim.run_time == 0.8
