"""Design token and theme system for Animora.

Manages color palettes, typography tokens, stroke widths, opacity levels,
and animation timing curves for consistent, accessible, and publication-ready
aesthetics across all visualizations.
"""

from __future__ import annotations

from animora.theme.builtin import (
    Cyberpunk,
    DefaultTheme,
    ModernDark,
    Monokai,
    PaperLight,
)
from animora.theme.context import (
    get_active_theme,
    set_active_theme,
    use_theme,
)
from animora.theme.theme import (
    AnimationTiming,
    ColorPalette,
    CornerRadius,
    SpacingScale,
    StrokeScale,
    Theme,
    Typography,
)

__all__: list[str] = [
    "AnimationTiming",
    "ColorPalette",
    "CornerRadius",
    "Cyberpunk",
    "DefaultTheme",
    "ModernDark",
    "Monokai",
    "PaperLight",
    "SpacingScale",
    "StrokeScale",
    "Theme",
    "Typography",
    "get_active_theme",
    "set_active_theme",
    "use_theme",
]
