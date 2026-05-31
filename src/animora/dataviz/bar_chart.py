"""BarChart data visualization component with animated bar reveals."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
import numpy as np
import manim

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


class BarChart(Component):
    """An animated bar chart component.

    Composes on top of Axes and Shape primitives, providing mathematical
    bar dimension scaling and animated reveals.

    Example:
    ```python
    chart = BarChart(data=[("Q1", 40), ("Q2", 65), ("Q3", 30)])
    scene.play(chart.animate_grow())
    ```
    """

    def __init__(
        self,
        data: Sequence[tuple[str, float]] | dict[str, float] | Sequence[float],
        *,
        axes: Axes | None = None,
        bar_width: float = 0.6,
        bar_color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        # Standardize data format to list of (label, value)
        if isinstance(data, dict):
            self._data: list[tuple[str, float]] = [(str(k), float(v)) for k, v in data.items()]
        elif data and isinstance(data[0], (tuple, list)):
            self._data = [(str(item[0]), float(item[1])) for item in data]  # type: ignore[index]
        else:
            self._data = [(f"Item {idx+1}", float(v)) for idx, v in enumerate(data)]  # type: ignore[arg-type]

        self._bar_width = float(bar_width)
        self._bar_color = bar_color

        # Auto-compute axes if not supplied
        if axes is None:
            max_val = max((v for _, v in self._data), default=10.0)
            y_ceil = float(np.ceil(max_val * 1.2)) if max_val > 0 else 10.0
            self._axes = Axes(
                x_range=(0, len(self._data) + 1, 1),
                y_range=(0, y_ceil, y_ceil / 5.0),
                x_length=8.0,
                y_length=5.0,
            )
        else:
            self._axes = axes

        self._bars: list[Shape] = []
        self._labels: list[Text] = []
        super().__init__(config=config, **kwargs)

    @property
    def axes(self) -> Axes:
        """The coordinate Axes used for mapping."""
        return self._axes

    @property
    def bars(self) -> list[Shape]:
        """List of Shape rectangle components representing the bars."""
        return list(self._bars)

    # -------------------------------------------------------------------------
    # Pure Data Transformation (Dual-Correctness Principle)
    # -------------------------------------------------------------------------
    @staticmethod
    def compute_bar_heights(
        values: Sequence[float],
        y_max: float,
        y_length: float,
    ) -> list[float]:
        """Compute visual bar heights in scene units for a list of values."""
        span = y_max if y_max > 0 else 1.0
        return [(val / span) * y_length for val in values]

    def _build_mobject(self) -> manim.Mobject:
        """Construct the Axes, Bars, and Category Labels."""
        active_theme = get_active_theme()
        bar_fill = self._bar_color or active_theme.colors.primary

        self._bars = []
        self._labels = []

        all_mobjects: list[manim.Mobject] = [self._axes.manim_object]

        for idx, (label_str, val) in enumerate(self._data):
            x_data = float(idx + 1)
            p_base = self._axes.c2p(x_data, 0.0)
            p_top = self._axes.c2p(x_data, val)

            bar_height = max(1e-3, float(abs(p_top[1] - p_base[1])))
            center_y = (p_base[1] + p_top[1]) / 2.0
            center_x = p_base[0]

            bar_shape = Shape.rounded_rectangle(
                width=self._bar_width,
                height=bar_height,
                corner_radius=0.08,
                fill_color=bar_fill,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.border,
                stroke_width=active_theme.strokes.thin,
            ).move_to([center_x, center_y, 0.0])

            lbl = Text(
                label_str,
                font_size=active_theme.typography.font_size_xs,
                color=active_theme.colors.text_muted,
            ).move_to([center_x, p_base[1] - 0.35, 0.0])

            self._bars.append(bar_shape)
            self._labels.append(lbl)

            all_mobjects.append(bar_shape.manim_object)
            all_mobjects.append(lbl.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_grow(self, run_time: float | None = None) -> Animation:
        """Animate bars growing from baseline."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        # Manim GrowFromPoint or Create
        bar_mobjects = [bar.manim_object for bar in self._bars]
        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(
                *[manim.GrowFromPoint(bm, bm.get_bottom()) for bm in bar_mobjects],
                run_time=duration,
            ),
            run_time=duration,
            name="grow_bars",
        )

    def animate_highlight_bar(
        self,
        index: int,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Highlight a specific bar."""
        active_theme = get_active_theme()
        highlight_color = color or active_theme.colors.accent
        duration = run_time or active_theme.timing.normal

        target_bar = self._bars[index]
        return Animation(
            component=target_bar,
            manim_animation=manim.Indicate(target_bar.manim_object, color=highlight_color),
            run_time=duration,
            name=f"highlight_bar({index})",
        )


__all__ = [
    "BarChart",
]
