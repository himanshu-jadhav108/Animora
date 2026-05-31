"""ScatterPlot data visualization component for displaying 2D point distributions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
import numpy as np
import manim

from animora.components.shape import Shape
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


class ScatterPlot(Component):
    """An animated scatter plot component.

    Composes on top of Axes and Shape.circle primitives, translating data coordinates
    into scene points and supporting staggered animated appearances.

    Example:
    ```python
    plot = ScatterPlot(points=[(1, 2), (2, 5), (3, 7), (4, 4), (5, 9)])
    scene.play(plot.animate_plot())
    ```
    """

    def __init__(
        self,
        points: Sequence[tuple[float, float]] | np.ndarray,
        *,
        axes: Axes | None = None,
        point_radius: float = 0.1,
        point_color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._raw_points: list[tuple[float, float]] = [
            (float(p[0]), float(p[1])) for p in points
        ]
        self._point_radius = float(point_radius)
        self._point_color = point_color

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

        self._dots: list[Shape] = []
        super().__init__(config=config, **kwargs)

    @property
    def axes(self) -> Axes:
        """The underlying coordinate Axes."""
        return self._axes

    @property
    def dots(self) -> list[Shape]:
        """List of Shape circular dot components."""
        return list(self._dots)

    # -------------------------------------------------------------------------
    # Pure Data Transformation
    # -------------------------------------------------------------------------
    @staticmethod
    def map_points(
        points: Sequence[tuple[float, float]],
        axes: Axes,
    ) -> list[np.ndarray]:
        """Transform data coordinates to 3D scene point vectors."""
        return [axes.c2p(x, y) for x, y in points]

    def _build_mobject(self) -> manim.Mobject:
        """Build the Axes and Dot primitives."""
        active_theme = get_active_theme()
        dot_fill = self._point_color or active_theme.colors.primary

        self._dots = []
        all_mobjects: list[manim.Mobject] = [self._axes.manim_object]

        for x, y in self._raw_points:
            pos = self._axes.c2p(x, y)
            dot = Shape.circle(
                radius=self._point_radius,
                fill_color=dot_fill,
                fill_opacity=1.0,
                stroke_color=active_theme.colors.border,
                stroke_width=active_theme.strokes.thin,
            ).move_to(pos)

            self._dots.append(dot)
            all_mobjects.append(dot.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_plot(self, run_time: float | None = None) -> Animation:
        """Animate the appearance of points."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        dot_mobjects = [d.manim_object for d in self._dots]
        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(
                *[manim.FadeIn(dm, scale=0.5) for dm in dot_mobjects],
                lag_ratio=0.1,
                run_time=duration,
            ),
            run_time=duration,
            name="plot_points",
        )


__all__ = [
    "ScatterPlot",
]
