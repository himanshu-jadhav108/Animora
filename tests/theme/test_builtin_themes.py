"""Unit tests for built-in themes completeness and aesthetics."""

from __future__ import annotations

from animora.theme.builtin import (
    Cyberpunk,
    DefaultTheme,
    ModernDark,
    Monokai,
    PaperLight,
)
from animora.theme.theme import Theme


def test_builtin_themes_presence() -> None:
    """Verify all built-in themes are valid Theme instances."""
    themes = [ModernDark, PaperLight, Cyberpunk, Monokai, DefaultTheme]
    for th in themes:
        assert isinstance(th, Theme)
        assert isinstance(th.colors.primary, str)
        assert isinstance(th.colors.background, str)
        assert isinstance(th.colors.text, str)
        assert th.colors.background.startswith("#")


def test_contrast_difference_between_dark_and_light() -> None:
    """Verify ModernDark and PaperLight have distinct background and text colors."""
    assert ModernDark.colors.background != PaperLight.colors.background
    assert ModernDark.colors.text != PaperLight.colors.text
    assert ModernDark.colors.background == "#0F172A"
    assert PaperLight.colors.background == "#FFFFFF"
