"""Arrow primitive component for directional flow and graph edges."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.connector import Connector
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class Arrow(Connector):
    """A directional arrow connector between components or coordinates.

    Composes on top of Connector, adding configurable arrowhead tips,
    straight/curved paths, and active theme styling.

    Example:
    ```python
    node_a = Shape.circle(radius=0.4).move_to([0, 2, 0])
    node_b = Shape.circle(radius=0.4).move_to([0, -2, 0])
    edge = Arrow(start=node_a, end=node_b)
    ```
    """

    def __init__(
        self,
        start: Component | Sequence[float] | np.ndarray,
        end: Component | Sequence[float] | np.ndarray,
        *,
        path_arc: float = 0.0,
        tip_length: float = 0.25,
        buff: float = 0.1,
        stroke_color: str | None = None,
        stroke_width: float | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        active_theme = get_active_theme()
        resolved_color = stroke_color if stroke_color is not None else active_theme.colors.primary
        resolved_width = stroke_width if stroke_width is not None else active_theme.strokes.thick

        self._tip_length: float = tip_length
        self._buff: float = buff
        super().__init__(
            start=start,
            end=end,
            path_arc=path_arc,
            stroke_color=resolved_color,
            stroke_width=resolved_width,
            config=config,
            **kwargs,
        )

    def _build_mobject(self) -> manim.Mobject:
        """Build underlying Manim Arrow or CurvedArrow."""
        p_start = self.start_point
        p_end = self.end_point
        stroke_col = self.config.stroke_color or self.config.color

        if abs(self._path_arc) > 1e-4:
            mob = manim.CurvedArrow(
                p_start,
                p_end,
                angle=self._path_arc,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                tip_length=self._tip_length,
            )
        else:
            mob = manim.Arrow(
                p_start,
                p_end,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                tip_length=self._tip_length,
                buff=self._buff,
                max_tip_length_to_length_ratio=0.3,
            )
        return mob

    def animate_highlight(
        self,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Animate highlighting the arrow (e.g. during traversal)."""
        active_theme = get_active_theme()
        highlight_color = color if color is not None else active_theme.colors.accent
        duration = run_time if run_time is not None else active_theme.timing.normal

        return Animation(
            component=self,
            manim_animation=manim.Indicate(self.manim_object, color=highlight_color),
            run_time=duration,
            name=f"highlight_arrow(color={highlight_color})",
        )


__all__ = [
    "Arrow",
]
