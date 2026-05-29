"""Unit tests for Theme structure, dataclasses, and merging."""

from __future__ import annotations

from animora.theme.theme import (
    AnimationTiming,
    ColorPalette,
    CornerRadius,
    SpacingScale,
    StrokeScale,
    Theme,
    Typography,
)


def test_theme_defaults() -> None:
    """Verify Theme dataclass default instantiation."""
    theme = Theme()
    assert isinstance(theme.colors, ColorPalette)
    assert isinstance(theme.typography, Typography)
    assert isinstance(theme.spacing, SpacingScale)
    assert isinstance(theme.strokes, StrokeScale)
    assert isinstance(theme.corner_radius, CornerRadius)
    assert isinstance(theme.timing, AnimationTiming)


def test_theme_merge_override() -> None:
    """Verify theme.merge() cleanly overrides specific tokens."""
    base_theme = Theme(name="base")
    custom = base_theme.merge(
        name="custom_theme",
        colors={"primary": "#FF0000", "accent": "#00FF00"},
        strokes={"thick": 6.0},
    )

    assert custom.name == "custom_theme"
    assert custom.colors.primary == "#FF0000"
    assert custom.colors.accent == "#00FF00"
    # Non-overridden color remains unchanged
    assert custom.colors.background == base_theme.colors.background
    assert custom.strokes.thick == 6.0
    assert custom.strokes.regular == base_theme.strokes.regular
