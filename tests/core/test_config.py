"""Unit tests for ComponentConfig and BoundingBox."""

from __future__ import annotations

from animora.core.config import BoundingBox, ComponentConfig


def test_bounding_box_geometry() -> None:
    """Verify BoundingBox width, height, depth, and center computations."""
    box = BoundingBox(min_point=(-2.0, -1.0, 0.0), max_point=(2.0, 3.0, 0.0))
    assert box.width == 4.0
    assert box.height == 4.0
    assert box.depth == 0.0
    assert box.center == (0.0, 1.0, 0.0)


def test_component_config_defaults() -> None:
    """Verify raw default values in ComponentConfig are None and resolve via theme."""
    from animora.theme.builtin import ModernDark

    cfg = ComponentConfig()
    assert cfg.color is None
    assert cfg.fill_color is None
    assert cfg.fill_opacity == 1.0
    assert cfg.stroke_color is None
    assert cfg.stroke_width is None
    assert cfg.font_size is None
    assert cfg.font_family is None
    assert cfg.extra_props == {}

    # Resolve with Theme fills unset fields from the active or specified theme
    resolved = cfg.resolve_with_theme(ModernDark)
    assert resolved.color == ModernDark.colors.text
    assert resolved.fill_color == ModernDark.colors.primary
    assert resolved.stroke_color == ModernDark.colors.border
    assert resolved.stroke_width == ModernDark.strokes.regular
    assert resolved.font_size == ModernDark.typography.font_size_md
    assert resolved.font_family == ModernDark.typography.font_family


def test_component_config_merge() -> None:
    """Verify merge method overrides properties without modifying original instance."""
    original = ComponentConfig(color="#FFFFFF", font_size=24.0)
    merged = original.merge(color="#FF0000", custom_attr=123)

    assert original.color == "#FFFFFF"
    assert merged.color == "#FF0000"
    assert merged.font_size == 24.0
    assert merged.extra_props.get("custom_attr") == 123
