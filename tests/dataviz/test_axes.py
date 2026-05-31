"""Unit tests for Axes coordinate mapping (c2p and p2c)."""

from __future__ import annotations

import numpy as np
import pytest
from animora.dataviz.axes import Axes


def test_axes_c2p_and_p2c_roundtrip() -> None:
    """Verify computational correctness and invertibility of c2p and p2c mapping."""
    axes = Axes(x_range=(0, 10, 1), y_range=(0, 100, 10), x_length=10.0, y_length=6.0)

    # Test test data coordinates
    test_coords = [(0.0, 0.0), (5.0, 50.0), (10.0, 100.0), (2.5, 75.0)]

    for x, y in test_coords:
        scene_pt = axes.c2p(x, y)
        assert isinstance(scene_pt, np.ndarray)
        assert len(scene_pt) == 3

        # Invert
        data_x, data_y = axes.p2c(scene_pt)
        assert pytest.approx(data_x, abs=1e-4) == x
        assert pytest.approx(data_y, abs=1e-4) == y


def test_axes_c2p_proportions() -> None:
    """Verify midpoint in data maps to midpoint in scene space."""
    axes = Axes(x_range=(0, 20, 5), y_range=(0, 100, 20), x_length=8.0, y_length=4.0)

    p_min = axes.c2p(0.0, 0.0)
    p_mid = axes.c2p(10.0, 50.0)
    p_max = axes.c2p(20.0, 100.0)

    # p_mid should be exactly the midpoint between p_min and p_max
    assert pytest.approx(p_mid[0], abs=1e-4) == (p_min[0] + p_max[0]) / 2.0
    assert pytest.approx(p_mid[1], abs=1e-4) == (p_min[1] + p_max[1]) / 2.0
    assert pytest.approx(p_max[0] - p_min[0], abs=1e-4) == 8.0
    assert pytest.approx(p_max[1] - p_min[1], abs=1e-4) == 4.0
