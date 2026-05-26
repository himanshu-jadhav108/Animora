"""Connector primitive component for connecting components and coordinate points."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
import numpy as np
import manim

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig

if TYPE_CHECKING:
    from typing_extensions import Self


class Connector(Component):
    """A geometric line or curved arc connecting two components or coordinate points.

    Supports straight lines and curved arcs with customizable stroke colors
    and widths.

    Example:
    ```python
    node_a = Shape.circle(radius=0.5).move_to([-2, 0, 0])
    node_b = Shape.circle(radius=0.5).move_to([2, 0, 0])
    link = Connector(start=node_a, end=node_b, stroke_color="#94A3B8")
    ```
    """

    def __init__(
        self,
        start: Component | Sequence[float] | np.ndarray,
        end: Component | Sequence[float] | np.ndarray,
        *,
        path_arc: float = 0.0,
        stroke_color: str | None = "#94A3B8",
        stroke_width: float = 2.5,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        cfg = config or ComponentConfig(
            color=stroke_color or "#94A3B8",
            stroke_color=stroke_color or "#94A3B8",
            stroke_width=stroke_width,
        )
        self._start_target = start
        self._end_target = end
        self._path_arc = float(path_arc)
        super().__init__(config=cfg, **kwargs)

    def _resolve_point(self, target: Component | Sequence[float] | np.ndarray) -> np.ndarray:
        """Resolve target to a 3D coordinate vector."""
        if isinstance(target, Component):
            return target.center
        return np.asarray(target, dtype=float)

    @property
    def start_point(self) -> np.ndarray:
        """The resolved 3D start coordinate."""
        return self._resolve_point(self._start_target)

    @property
    def end_point(self) -> np.ndarray:
        """The resolved 3D end coordinate."""
        return self._resolve_point(self._end_target)

    def _build_mobject(self) -> manim.Mobject:
        """Build Manim Line or ArcBetweenPoints connecting start and end."""
        p_start = self.start_point
        p_end = self.end_point
        stroke_col = self.config.stroke_color or self.config.color

        if abs(self._path_arc) > 1e-4:
            mob = manim.ArcBetweenPoints(
                p_start,
                p_end,
                angle=self._path_arc,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
            )
        else:
            mob = manim.Line(
                p_start,
                p_end,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                buff=0.0,
            )
        return mob

    def animate_draw(self, run_time: float = 1.0) -> Animation:
        """Animate drawing the connector from start to end."""
        return Animation(
            component=self,
            manim_animation=manim.Create(self.manim_object),
            run_time=run_time,
            name="draw_connector",
        )


__all__ = [
    "Connector",
]
