"""Grid layout solver arranging items in a 2D matrix of rows and columns."""

from __future__ import annotations

import math
from typing import Any, Sequence

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class GridLayout(BaseLayout):
    """Arranges layout items in a uniform 2D grid matrix of rows and columns.

    Example:
    ```python
    layout = GridLayout(columns=3, col_spacing=0.5, row_spacing=0.5)
    result = layout.solve(items)
    ```
    """

    def __init__(
        self,
        rows: int | None = None,
        columns: int | None = None,
        col_spacing: float = 0.5,
        row_spacing: float = 0.5,
        center_origin: bool = True,
    ) -> None:
        if rows is None and columns is None:
            columns = 3  # default 3 columns
        self.rows = rows
        self.columns = columns
        self.col_spacing = float(col_spacing)
        self.row_spacing = float(row_spacing)
        self.center_origin = center_origin

    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        if not items:
            return LayoutResult(positions={}, total_width=0.0, total_height=0.0)

        n = len(items)
        if self.columns is not None:
            cols = max(1, self.columns)
            rows = max(1, math.ceil(n / cols))
        elif self.rows is not None:
            rows = max(1, self.rows)
            cols = max(1, math.ceil(n / rows))
        else:
            cols = 3
            rows = math.ceil(n / cols)

        # 1. Determine maximum cell width and height across all items
        cell_w = max(item.width for item in items)
        cell_h = max(item.height for item in items)

        # 2. Total dimensions
        total_w = (cols * cell_w) + (max(0, cols - 1) * self.col_spacing)
        total_h = (rows * cell_h) + (max(0, rows - 1) * self.row_spacing)

        # 3. Origin offsets
        start_x = (-total_w / 2.0) + (cell_w / 2.0) if self.center_origin else (cell_w / 2.0)
        start_y = (total_h / 2.0) - (cell_h / 2.0) if self.center_origin else total_h - (cell_h / 2.0)

        positions: dict[str, tuple[float, float, float]] = {}
        for idx, item in enumerate(items):
            r = idx // cols
            c = idx % cols

            x = start_x + (c * (cell_w + self.col_spacing))
            y = start_y - (r * (cell_h + self.row_spacing))

            positions[item.id] = (x, y, 0.0)

        return LayoutResult(
            positions=positions,
            total_width=total_w,
            total_height=total_h,
        )


__all__ = [
    "GridLayout",
]
