"""Unit tests for TensorGrid component."""

from __future__ import annotations

import numpy as np

from animora.ml.tensor_grid import TensorGrid


def test_tensor_grid_structure() -> None:
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    grid = TensorGrid(data, title="Sample Matrix")

    assert grid.num_rows == 2
    assert grid.num_cols == 3
    assert len(grid.cells) == 2
    assert len(grid.cells[0]) == 3


def test_tensor_grid_highlight_animation() -> None:
    data = [[0.1, 0.9], [0.8, 0.2]]
    grid = TensorGrid(data)

    anim = grid.animate_highlight_cell(0, 1, run_time=0.4)
    assert "highlight_cell_0_1" in anim.name
    assert anim.run_time == 0.4
