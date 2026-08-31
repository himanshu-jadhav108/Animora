"""Shape primitive component covering circles, rectangles, and polygons."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import TYPE_CHECKING, Any

import manim

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class ShapeType(str, Enum):
    """Enumeration of geometric shape types supported by Shape."""

    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    ROUNDED_RECTANGLE = "rounded_rectangle"
    POLYGON = "polygon"


class Shape(Component):
    """A versatile geometric shape primitive component.

    Supports circles, rectangles, rounded rectangles, and arbitrary polygons
    with rich fill styling, stroke borders, and theme resolution.

    Example:
    ```python
    circle_node = Shape.circle(radius=0.6)
    rect_card = Shape.rectangle(width=3.0, height=1.5)
    ```
    """

    def __init__(
        self,
        shape_type: ShapeType = ShapeType.RECTANGLE,
        *,
        radius: float = 0.5,
        width: float = 2.0,
        height: float = 1.0,
        corner_radius: float | None = None,
        vertices: Sequence[Sequence[float]] | None = None,
        fill_color: str | None = None,
        fill_opacity: float = 0.8,
        stroke_color: str | None = None,
        stroke_width: float | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        active_theme = get_active_theme()

        resolved_fill = fill_color if fill_color is not None else active_theme.colors.primary
        resolved_stroke = stroke_color if stroke_color is not None else active_theme.colors.border
        resolved_stroke_w = (
            stroke_width if stroke_width is not None else active_theme.strokes.regular
        )
        resolved_corner_r = (
            corner_radius if corner_radius is not None else active_theme.corner_radius.md
        )

        cfg = config or ComponentConfig(
            color=resolved_stroke,
            fill_color=resolved_fill,
            fill_opacity=fill_opacity,
            stroke_color=resolved_stroke,
            stroke_width=resolved_stroke_w,
        )

        self._shape_type: ShapeType = shape_type
        self._radius: float = radius
        self._custom_width: float = width
        self._custom_height: float = height
        self._corner_radius: float = resolved_corner_r
        self._vertices: Sequence[Sequence[float]] | None = vertices
        super().__init__(config=cfg, **kwargs)

    @classmethod
    def circle(
        cls,
        radius: float = 0.5,
        *,
        fill_color: str | None = None,
        fill_opacity: float = 0.8,
        stroke_color: str | None = None,
        stroke_width: float | None = None,
        **kwargs: Any,
    ) -> Shape:
        """Construct a circular shape component."""
        return cls(
            shape_type=ShapeType.CIRCLE,
            radius=radius,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            **kwargs,
        )

    @classmethod
    def rectangle(
        cls,
        width: float = 2.0,
        height: float = 1.0,
        *,
        fill_color: str | None = None,
        fill_opacity: float = 0.8,
        stroke_color: str | None = None,
        stroke_width: float | None = None,
        **kwargs: Any,
    ) -> Shape:
        """Construct a rectangular shape component."""
        return cls(
            shape_type=ShapeType.RECTANGLE,
            width=width,
            height=height,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            **kwargs,
        )

    @classmethod
    def rounded_rectangle(
        cls,
        width: float = 2.0,
        height: float = 1.0,
        corner_radius: float | None = None,
        *,
        fill_color: str | None = None,
        fill_opacity: float = 0.8,
        stroke_color: str | None = None,
        stroke_width: float | None = None,
        **kwargs: Any,
    ) -> Shape:
        """Construct a rounded rectangular shape component."""
        return cls(
            shape_type=ShapeType.ROUNDED_RECTANGLE,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            **kwargs,
        )

    @classmethod
    def polygon(
        cls,
        vertices: Sequence[Sequence[float]],
        *,
        fill_color: str | None = None,
        fill_opacity: float = 0.8,
        stroke_color: str | None = None,
        stroke_width: float | None = None,
        **kwargs: Any,
    ) -> Shape:
        """Construct an arbitrary polygon shape component from vertex coordinates."""
        return cls(
            shape_type=ShapeType.POLYGON,
            vertices=vertices,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            **kwargs,
        )

    def _build_mobject(self) -> manim.Mobject:
        """Build underlying Manim VMobject based on shape type and parameters."""
        fill_col = self.config.fill_color or self.config.color
        stroke_col = self.config.stroke_color or self.config.color

        if self._shape_type == ShapeType.CIRCLE:
            mob = manim.Circle(
                radius=self._radius,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                fill_color=fill_col,
                fill_opacity=self.config.fill_opacity,
            )
        elif self._shape_type == ShapeType.ROUNDED_RECTANGLE:
            mob = manim.RoundedRectangle(
                corner_radius=self._corner_radius,
                width=self._custom_width,
                height=self._custom_height,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                fill_color=fill_col,
                fill_opacity=self.config.fill_opacity,
            )
        elif self._shape_type == ShapeType.POLYGON and self._vertices is not None:
            mob = manim.Polygon(
                *self._vertices,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                fill_color=fill_col,
                fill_opacity=self.config.fill_opacity,
            )
        else:  # RECTANGLE default
            mob = manim.Rectangle(
                width=self._custom_width,
                height=self._custom_height,
                color=stroke_col,
                stroke_width=self.config.stroke_width,
                fill_color=fill_col,
                fill_opacity=self.config.fill_opacity,
            )

        return mob

    def animate_highlight(
        self,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Animate highlighting the shape with an emphasis color."""
        active_theme = get_active_theme()
        highlight_color = color if color is not None else active_theme.colors.accent
        duration = run_time if run_time is not None else active_theme.timing.normal

        return Animation(
            component=self,
            manim_animation=manim.Indicate(self.manim_object, color=highlight_color),
            run_time=duration,
            name=f"highlight(color={highlight_color})",
        )


__all__ = [
    "Shape",
    "ShapeType",
]
