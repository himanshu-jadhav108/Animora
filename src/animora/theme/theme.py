"""Design token data structures and Theme specification for Animora."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class ColorPalette:
    """Color palette design tokens defining semantic UI and data roles."""

    primary: str = "#38BDF8"
    secondary: str = "#818CF8"
    accent: str = "#F59E0B"
    background: str = "#0F172A"
    surface: str = "#1E293B"
    text: str = "#F8FAFC"
    text_muted: str = "#94A3B8"
    border: str = "#334155"
    success: str = "#10B981"
    warning: str = "#F59E0B"
    error: str = "#EF4444"


@dataclass(frozen=True)
class Typography:
    """Typography design tokens defining font sizes and families."""

    font_family: str | None = None
    font_size_xs: float = 18.0
    font_size_sm: float = 24.0
    font_size_md: float = 32.0
    font_size_lg: float = 40.0
    font_size_xl: float = 48.0
    line_spacing: float = 1.0


@dataclass(frozen=True)
class SpacingScale:
    """Spacing scale tokens in Manim scene units."""

    xs: float = 0.1
    sm: float = 0.25
    md: float = 0.5
    lg: float = 1.0
    xl: float = 2.0


@dataclass(frozen=True)
class StrokeScale:
    """Stroke width tokens."""

    thin: float = 1.0
    regular: float = 2.5
    thick: float = 4.0


@dataclass(frozen=True)
class CornerRadius:
    """Corner radius tokens for rounded shapes and containers."""

    none: float = 0.0
    sm: float = 0.1
    md: float = 0.2
    lg: float = 0.4
    full: float = 0.8


@dataclass(frozen=True)
class AnimationTiming:
    """Animation duration and easing curve tokens."""

    fast: float = 0.4
    normal: float = 1.0
    slow: float = 2.0


@dataclass(frozen=True)
class Theme:
    """Complete design token specification for Animora scenes and components."""

    name: str = "custom"
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    spacing: SpacingScale = field(default_factory=SpacingScale)
    strokes: StrokeScale = field(default_factory=StrokeScale)
    corner_radius: CornerRadius = field(default_factory=CornerRadius)
    timing: AnimationTiming = field(default_factory=AnimationTiming)

    def merge(
        self,
        name: str | None = None,
        colors: ColorPalette | dict[str, str] | None = None,
        typography: Typography | dict[str, Any] | None = None,
        spacing: SpacingScale | dict[str, float] | None = None,
        strokes: StrokeScale | dict[str, float] | None = None,
        corner_radius: CornerRadius | dict[str, float] | None = None,
        timing: AnimationTiming | dict[str, Any] | None = None,
    ) -> Theme:
        """Return a new Theme instance with specified token overrides."""
        new_colors = (
            replace(self.colors, **colors) if isinstance(colors, dict) else (colors or self.colors)
        )
        new_typography = (
            replace(self.typography, **typography)
            if isinstance(typography, dict)
            else (typography or self.typography)
        )
        new_spacing = (
            replace(self.spacing, **spacing)
            if isinstance(spacing, dict)
            else (spacing or self.spacing)
        )
        new_strokes = (
            replace(self.strokes, **strokes)
            if isinstance(strokes, dict)
            else (strokes or self.strokes)
        )
        new_corners = (
            replace(self.corner_radius, **corner_radius)
            if isinstance(corner_radius, dict)
            else (corner_radius or self.corner_radius)
        )
        new_timing = (
            replace(self.timing, **timing) if isinstance(timing, dict) else (timing or self.timing)
        )

        return Theme(
            name=name or f"{self.name}_modified",
            colors=new_colors,
            typography=new_typography,
            spacing=new_spacing,
            strokes=new_strokes,
            corner_radius=new_corners,
            timing=new_timing,
        )


__all__ = [
    "AnimationTiming",
    "ColorPalette",
    "CornerRadius",
    "SpacingScale",
    "StrokeScale",
    "Theme",
    "Typography",
]
