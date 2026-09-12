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
from animora.theme.effects import (
    Aurora,
    BaseEffect,
    apply_effect,
    get_effect,
    register_effect,
)
from animora.theme.presets import (
    CINEMATIC,
    EDUCATIONAL,
    PLAYFUL,
    PRESETS,
    SLOW_MO,
    SMOOTH,
    SNAPPY,
    TimingPreset,
    get_timing_preset,
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
    "CINEMATIC",
    "EDUCATIONAL",
    "PLAYFUL",
    "PRESETS",
    "SLOW_MO",
    "SMOOTH",
    "SNAPPY",
    "AnimationTiming",
    "Aurora",
    "BaseEffect",
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
    "TimingPreset",
    "Typography",
    "apply_effect",
    "get_active_theme",
    "get_effect",
    "get_timing_preset",
    "register_effect",
    "set_active_theme",
    "use_theme",
]
