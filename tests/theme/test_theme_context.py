"""Unit tests for active theme context management and primitive resolution."""

from __future__ import annotations

from animora.components.shape import Shape
from animora.components.text import Text
from animora.theme.builtin import Cyberpunk, DefaultTheme, PaperLight
from animora.theme.context import get_active_theme, set_active_theme, use_theme


def test_theme_context_manager() -> None:
    """Verify use_theme switches active theme and restores on exit."""
    assert get_active_theme() == DefaultTheme

    with use_theme(PaperLight):
        assert get_active_theme() == PaperLight

        with use_theme(Cyberpunk):
            assert get_active_theme() == Cyberpunk

        assert get_active_theme() == PaperLight

    assert get_active_theme() == DefaultTheme


def test_primitive_resolves_active_theme() -> None:
    """Verify primitives constructed inside use_theme adopt active theme defaults."""
    with use_theme(PaperLight):
        txt = Text("Light Text")
        assert txt.config.color == PaperLight.colors.text
        circle = Shape.circle()
        assert circle.config.fill_color == PaperLight.colors.primary

    with use_theme(Cyberpunk):
        txt_cyber = Text("Cyber Text")
        assert txt_cyber.config.color == Cyberpunk.colors.text
        circle_cyber = Shape.circle()
        assert circle_cyber.config.fill_color == Cyberpunk.colors.primary


def test_explicit_override_wins_over_theme() -> None:
    """Verify explicit parameters always take precedence over theme defaults."""
    with use_theme(Cyberpunk):
        # Override fill_color explicitly
        circle = Shape.circle(fill_color="#ABCDEF")
        assert circle.config.fill_color == "#ABCDEF"
        # Other non-overridden properties still resolve from active theme
        assert circle.config.stroke_color == Cyberpunk.colors.border
