"""Table component displaying 2D tabular data arranged via GridLayout."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
import manim

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.grid import GridLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


class Table(Component):
    """A tabular data visualization component.

    Renders structured rows and columns using GridLayout from Phase 4,
    supporting cell styling, header distinction, and cell/row highlighting animations.

    Example:
    ```python
    table = Table(
        data=[["Alice", 95], ["Bob", 88], ["Charlie", 92]],
        headers=["Name", "Score"],
    )
    ```
    """

    def __init__(
        self,
        data: Sequence[Sequence[Any]],
        headers: Sequence[str] | None = None,
        *,
        cell_width: float = 2.2,
        cell_height: float = 0.8,
        col_spacing: float = 0.05,
        row_spacing: float = 0.05,
        header_color: str | None = None,
        cell_color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._data: list[list[str]] = [[str(val) for val in row] for row in data]
        self._headers: list[str] | None = [str(h) for h in headers] if headers else None
        self._cell_width = float(cell_width)
        self._cell_height = float(cell_height)
        self._col_spacing = float(col_spacing)
        self._row_spacing = float(row_spacing)
        self._header_color = header_color
        self._cell_color = cell_color

        # Grid of cell components: cell_grid[row][col] -> Group(bg_shape, text)
        self._cells: list[list[Group]] = []

        super().__init__(config=config, **kwargs)

    @property
    def num_rows(self) -> int:
        """Total number of data rows."""
        return len(self._data)

    @property
    def num_cols(self) -> int:
        """Total number of columns."""
        if self._headers:
            return len(self._headers)
        return len(self._data[0]) if self._data else 0

    def get_cell(self, row: int, col: int) -> Group:
        """Get the composite cell component at the given row and column index."""
        return self._cells[row][col]

    def _build_mobject(self) -> manim.Mobject:
        """Construct the table cells and arrange them in a 2D matrix using GridLayout."""
        active_theme = get_active_theme()

        all_row_data: list[list[str]] = []
        is_header_row: list[bool] = []

        if self._headers:
            all_row_data.append(self._headers)
            is_header_row.append(True)

        for row in self._data:
            all_row_data.append(row)
            is_header_row.append(False)

        num_cols = self.num_cols
        flat_cell_components: list[Group] = []
        self._cells = []

        for r_idx, (row, is_header) in enumerate(zip(all_row_data, is_header_row)):
            row_cells: list[Group] = []
            for c_idx, cell_value in enumerate(row):
                bg_color = (
                    self._header_color
                    or active_theme.colors.primary
                    if is_header
                    else (self._cell_color or active_theme.colors.surface)
                )
                txt_color = (
                    "#FFFFFF"
                    if is_header
                    else active_theme.colors.text
                )

                bg_rect = Shape.rounded_rectangle(
                    width=self._cell_width,
                    height=self._cell_height,
                    corner_radius=0.05,
                    fill_color=bg_color,
                    fill_opacity=0.9,
                    stroke_color=active_theme.colors.border,
                    stroke_width=active_theme.strokes.thin,
                )
                cell_text = Text(
                    cell_value,
                    font_size=active_theme.typography.font_size_sm if not is_header else active_theme.typography.font_size_sm + 2,
                    color=txt_color,
                )

                cell_grp = Group(bg_rect, cell_text)
                row_cells.append(cell_grp)
                flat_cell_components.append(cell_grp)

            self._cells.append(row_cells)

        # Use GridLayout from Phase 4 to compute coordinates
        grid_container = Group(*flat_cell_components)
        grid_container.arrange(
            GridLayout(
                columns=num_cols,
                col_spacing=self._col_spacing,
                row_spacing=self._row_spacing,
                center_origin=True,
            )
        )

        return grid_container.manim_object

    def animate_highlight_cell(
        self,
        row: int,
        col: int,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Animate highlighting a specific cell."""
        active_theme = get_active_theme()
        highlight_color = color or active_theme.colors.accent
        duration = run_time or active_theme.timing.normal

        target_cell = self._cells[row][col]
        return Animation(
            component=target_cell,
            manim_animation=manim.Indicate(target_cell.manim_object, color=highlight_color),
            run_time=duration,
            name=f"highlight_cell({row}, {col})",
        )


__all__ = [
    "Table",
]
