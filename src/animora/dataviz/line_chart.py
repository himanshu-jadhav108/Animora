"""LineChart data visualization component with progressive path reveals."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.connector import Connector
from animora.components.shape import Shape
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class LineChart(Component):
    """An animated line chart component connecting continuous data points.

    Composes on top of Axes, Connector, and Shape primitives, providing
    progressive line-draw animations and vertex markers.

    Example:
    ```python
    chart = LineChart(points=[(0, 10), (1, 25), (2, 18), (3, 42), (4, 30)])
    scene.play(chart.animate_draw())
    ```
    """

    def __init__(
        self,
        points: Sequence[tuple[float, float]] | np.ndarray,
        *,
        axes: Axes | None = None,
        line_color: str | None = None,
        stroke_width: float | None = None,
        show_dots: bool = True,
        dot_radius: float = 0.08,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._raw_points: list[tuple[float, float]] = [(float(p[0]), float(p[1])) for p in points]
        self._line_color = line_color
        self._custom_stroke_width = stroke_width
        self._show_dots = show_dots
        self._dot_radius = float(dot_radius)

        if axes is None:
            xs = [p[0] for p in self._raw_points] or [0.0]
            ys = [p[1] for p in self._raw_points] or [0.0]
            x_max = float(np.ceil(max(xs) * 1.2)) if max(xs) > 0 else 10.0
            y_max = float(np.ceil(max(ys) * 1.2)) if max(ys) > 0 else 10.0
            self._axes = Axes(
                x_range=(0, x_max, x_max / 5.0),
                y_range=(0, y_max, y_max / 5.0),
                x_length=8.0,
                y_length=5.0,
            )
        else:
            self._axes = axes

        self._lines: list[Connector] = []
        self._dots: list[Shape] = []
        super().__init__(config=config, **kwargs)

    @property
    def axes(self) -> Axes:
        """The underlying coordinate Axes."""
        return self._axes

    def _build_mobject(self) -> manim.Mobject:
        """Construct the Axes, Line segments, and vertex Dots."""
        active_theme = get_active_theme()
        stroke_col = self._line_color or active_theme.colors.primary
        stroke_w = self._custom_stroke_width or active_theme.strokes.regular

        self._lines = []
        self._dots = []
        all_mobjects: list[manim.Mobject] = [self._axes.manim_object]

        scene_pts = [self._axes.c2p(x, y) for x, y in self._raw_points]

        # Build connecting line segments
        for i in range(len(scene_pts) - 1):
            conn = Connector(
                start=scene_pts[i],
                end=scene_pts[i + 1],
                stroke_color=stroke_col,
                stroke_width=stroke_w,
            )
            self._lines.append(conn)
            all_mobjects.append(conn.manim_object)

        # Build vertex dots if enabled
        if self._show_dots:
            for pt in scene_pts:
                dot = Shape.circle(
                    radius=self._dot_radius,
                    fill_color=stroke_col,
                    fill_opacity=1.0,
                    stroke_color=active_theme.colors.background,
                    stroke_width=1.5,
                ).move_to(pt)
                self._dots.append(dot)
                all_mobjects.append(dot.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_draw(self, run_time: float | None = None) -> Animation:
        """Animate drawing the continuous line segments and dots."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.slow

        line_mobjects = [line.manim_object for line in self._lines]
        dot_mobjects = [dot.manim_object for dot in self._dots]

        animations: list[manim.Animation] = [manim.Create(lm) for lm in line_mobjects]
        if dot_mobjects:
            animations.append(manim.FadeIn(manim.VGroup(*dot_mobjects)))

        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(*animations, lag_ratio=0.1, run_time=duration),
            run_time=duration,
            name="draw_line_chart",
        )


__all__ = [
    "LineChart",
]
