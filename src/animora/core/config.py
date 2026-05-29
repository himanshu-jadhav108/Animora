"""Configuration and visual token definitions for Animora components."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from animora.theme.theme import Theme


@dataclass(frozen=True)
class BoundingBox:
    """Represents a 3D axis-aligned bounding box for a component."""

    min_point: tuple[float, float, float]
    max_point: tuple[float, float, float]

    @property
    def width(self) -> float:
        """Width along the X axis."""
        return abs(self.max_point[0] - self.min_point[0])

    @property
    def height(self) -> float:
        """Height along the Y axis."""
        return abs(self.max_point[1] - self.min_point[1])

    @property
    def depth(self) -> float:
        """Depth along the Z axis."""
        return abs(self.max_point[2] - self.min_point[2])

    @property
    def center(self) -> tuple[float, float, float]:
        """Geometric center point (x, y, z)."""
        return (
            (self.min_point[0] + self.max_point[0]) / 2.0,
            (self.min_point[1] + self.max_point[1]) / 2.0,
            (self.min_point[2] + self.max_point[2]) / 2.0,
        )


@dataclass
class ComponentConfig:
    """Visual configuration base for Animora components.

    Resolves styling tokens dynamically from the active Theme context unless
    explicitly overridden per component.
    """

    color: str | None = None
    fill_color: str | None = None
    fill_opacity: float = 1.0
    stroke_color: str | None = None
    stroke_width: float | None = None
    font_size: float | None = None
    font_family: str | None = None
    extra_props: dict[str, Any] = field(default_factory=dict)

    def resolve_with_theme(self, theme: Theme | None = None) -> ComponentConfig:
        """Resolve any unassigned (None) attributes against the provided or active theme."""
        if theme is None:
            from animora.theme.context import get_active_theme
            theme = get_active_theme()

        return ComponentConfig(
            color=self.color if self.color is not None else theme.colors.text,
            fill_color=self.fill_color if self.fill_color is not None else theme.colors.primary,
            fill_opacity=self.fill_opacity,
            stroke_color=self.stroke_color if self.stroke_color is not None else theme.colors.border,
            stroke_width=self.stroke_width if self.stroke_width is not None else theme.strokes.regular,
            font_size=self.font_size if self.font_size is not None else theme.typography.font_size_md,
            font_family=self.font_family if self.font_family is not None else theme.typography.font_family,
            extra_props=dict(self.extra_props),
        )

    def merge(self, **overrides: Any) -> ComponentConfig:
        """Return a new ComponentConfig with overridden properties."""
        current_data = {
            "color": self.color,
            "fill_color": self.fill_color,
            "fill_opacity": self.fill_opacity,
            "stroke_color": self.stroke_color,
            "stroke_width": self.stroke_width,
            "font_size": self.font_size,
            "font_family": self.font_family,
            "extra_props": dict(self.extra_props),
        }
        for k, v in overrides.items():
            if k in current_data:
                current_data[k] = v
            else:
                current_data["extra_props"][k] = v  # type: ignore[index]
        return ComponentConfig(**current_data)


__all__ = [
    "BoundingBox",
    "ComponentConfig",
]
