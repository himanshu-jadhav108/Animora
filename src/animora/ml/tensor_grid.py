"""TensorGrid component for 2D matrix, weight tensor, and attention score visualization."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.layout.grid import GridLayout
from animora.ml.base import MLComponent
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class TensorGrid(MLComponent):
    """Visualizes 2D matrices, weight tensors, and attention heatmaps.

    Reuses `GridLayout` for structured alignment and `Shape`/`Text` primitives
    for cell representation and dynamic value formatting.

    Example:
    ```python
    weights = np.array([[0.5, -0.2], [0.8, 0.1]])
    grid = TensorGrid(weights, title="Layer 1 Weights")
    ```
    """

    def __init__(
        self,
        values: Sequence[Sequence[float]] | np.ndarray,
        *,
        row_labels: Sequence[str] | None = None,
        col_labels: Sequence[str] | None = None,
        title: str | None = None,
        cell_size: float = 0.75,
        cell_spacing: float = 0.08,
        show_values: bool = True,
        value_format: str = "{:.2f}",
        colormap: Sequence[str] | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.values_matrix: np.ndarray = np.asarray(values, dtype=float)
        if self.values_matrix.ndim == 1:
            self.values_matrix = self.values_matrix.reshape(1, -1)

        self.num_rows, self.num_cols = self.values_matrix.shape
        self.row_labels = list(row_labels) if row_labels is not None else None
        self.col_labels = list(col_labels) if col_labels is not None else None
        self.title_text = title
        self.cell_size = float(cell_size)
        self.cell_spacing = float(cell_spacing)
        self.show_values = show_values
        self.value_format = value_format

        active_theme = get_active_theme()
        default_cmap = [
            active_theme.colors.surface,
            active_theme.colors.primary,
            active_theme.colors.secondary,
        ]
        self.colormap = list(colormap) if colormap is not None else default_cmap

        self.cells: list[list[Shape]] = []
        self.value_texts: list[list[Text]] = []

        super().__init__(config=config, **kwargs)

    def _interpolate_color(self, val: float, v_min: float, v_max: float) -> str:
        """Map value to color along theme colormap."""
        span = v_max - v_min if abs(v_max - v_min) > 1e-6 else 1.0
        norm_v = np.clip((val - v_min) / span, 0.0, 1.0)
        idx = min(int(norm_v * (len(self.colormap) - 1)), len(self.colormap) - 1)
        return self.colormap[idx]

    def _build_mobject(self) -> manim.Mobject:
        """Construct Manim composite mobject using GridLayout and visual primitives."""
        active_theme = get_active_theme()
        v_min = float(np.min(self.values_matrix)) if self.values_matrix.size > 0 else 0.0
        v_max = float(np.max(self.values_matrix)) if self.values_matrix.size > 0 else 1.0

        all_cell_components: list[Shape] = []
        self.cells = []
        self.value_texts = []

        for r in range(self.num_rows):
            row_cells: list[Shape] = []
            row_texts: list[Text] = []
            for c in range(self.num_cols):
                val = float(self.values_matrix[r, c])
                cell_color = self._interpolate_color(val, v_min, v_max)

                cell_shape = Shape.rounded_rectangle(
                    width=self.cell_size,
                    height=self.cell_size,
                    corner_radius=0.08,
                    fill_color=cell_color,
                    fill_opacity=0.45,
                    stroke_color=active_theme.colors.border,
                    stroke_width=active_theme.strokes.thin,
                )
                row_cells.append(cell_shape)
                all_cell_components.append(cell_shape)

                if self.show_values:
                    txt = Text(
                        self.value_format.format(val),
                        font_size=18,
                        color=active_theme.colors.text,
                    )
                    row_texts.append(txt)

            self.cells.append(row_cells)
            self.value_texts.append(row_texts)

        # Arrange cells using GridLayout
        cell_group = Group(*all_cell_components)
        cell_group.arrange(
            GridLayout(
                columns=self.num_cols,
                col_spacing=self.cell_spacing,
                row_spacing=self.cell_spacing,
            )
        )

        # Composite group
        composite = manim.VGroup(cell_group.manim_object)

        # Position value texts over cell centers
        if self.show_values:
            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    cell_pos = self.cells[r][c].center
                    txt_comp = self.value_texts[r][c]
                    txt_comp.move_to(cell_pos)
                    composite.add(txt_comp.manim_object)

        # Title
        if self.title_text:
            title_comp = Text(self.title_text, font_size=24, color=active_theme.colors.primary)
            total_h = self.num_rows * (self.cell_size + self.cell_spacing)
            grid_top = cell_group.center[1] + (total_h / 2.0)
            title_comp.move_to([cell_group.center[0], grid_top + 0.5, 0.0])
            composite.add(title_comp.manim_object)

        return composite

    def animate_highlight_cell(
        self,
        row: int,
        col: int,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Animate highlighting an individual tensor cell."""
        active_theme = get_active_theme()
        resolved_color = color or active_theme.colors.accent
        duration = run_time if run_time is not None else active_theme.timing.fast
        target_cell = self.cells[row][col]

        return Animation(
            component=target_cell,
            manim_animation=manim.Indicate(target_cell.manim_object, color=resolved_color),
            run_time=duration,
            name=f"highlight_cell_{row}_{col}",
        )


__all__ = [
    "TensorGrid",
]
