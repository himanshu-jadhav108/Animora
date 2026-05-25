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
    """Verify default values in ComponentConfig."""
    cfg = ComponentConfig()
    assert cfg.color == "#FFFFFF"
    assert cfg.fill_opacity == 1.0
    assert cfg.stroke_width == 2.0
    assert cfg.font_size == 36.0


def test_component_config_merge() -> None:
    """Verify merge method overrides properties without modifying original instance."""
    original = ComponentConfig(color="#FFFFFF", font_size=24.0)
    merged = original.merge(color="#FF0000", custom_attr=123)

    assert original.color == "#FFFFFF"
    assert merged.color == "#FF0000"
    assert merged.font_size == 24.0
    assert merged.extra_props.get("custom_attr") == 123
