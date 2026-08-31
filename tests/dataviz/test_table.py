"""Unit tests for Table data visualization component."""

from __future__ import annotations

from animora.core.animation import Animation
from animora.dataviz.table import Table


def test_table_dimensions_and_cells() -> None:
    """Verify Table rows, cols, and cell indexing."""
    data = [
        ["Alice", "95", "A"],
        ["Bob", "82", "B"],
        ["Charlie", "90", "A"],
    ]
    headers = ["Name", "Score", "Grade"]

    table = Table(data=data, headers=headers)
    assert table.num_rows == 3
    assert table.num_cols == 3

    # Total rows in grid = 1 header + 3 data = 4 rows
    assert len(table._cells) == 4
    # Header cell 0,0
    header_cell = table.get_cell(0, 0)
    assert header_cell is not None


def test_table_highlight_animation() -> None:
    """Verify table cell highlight returns valid Animation."""
    data = [["1", "2"], ["3", "4"]]
    table = Table(data=data)

    anim = table.animate_highlight_cell(0, 0, color="#F59E0B")
    assert isinstance(anim, Animation)
    assert anim.name == "highlight_cell(0, 0)"
