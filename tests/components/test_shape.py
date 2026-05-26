"""Unit tests for the Shape primitive component."""

from __future__ import annotations

import manim
import pytest

from animora.components.shape import Shape, ShapeType
from animora.core.animation import Animation


def test_shape_circle_factory() -> None:
    """Verify Shape.circle creates Circle VMobject with correct radius and styling."""
    circle = Shape.circle(radius=0.75, fill_color="#3B82F6", stroke_color="#FFFFFF")

    assert circle._shape_type == ShapeType.CIRCLE
    assert isinstance(circle.manim_object, manim.Circle)
    assert pytest.approx(circle.width, abs=1e-2) == 1.5
    assert pytest.approx(circle.height, abs=1e-2) == 1.5


def test_shape_rectangle_factory() -> None:
    """Verify Shape.rectangle creates Rectangle VMobject."""
    rect = Shape.rectangle(width=3.0, height=1.5, fill_color="#1E293B")

    assert rect._shape_type == ShapeType.RECTANGLE
    assert isinstance(rect.manim_object, manim.Rectangle)
    assert pytest.approx(rect.width, abs=1e-2) == 3.0
    assert pytest.approx(rect.height, abs=1e-2) == 1.5


def test_shape_rounded_rectangle_factory() -> None:
    """Verify Shape.rounded_rectangle creates RoundedRectangle VMobject."""
    round_rect = Shape.rounded_rectangle(width=4.0, height=2.0, corner_radius=0.3)

    assert round_rect._shape_type == ShapeType.ROUNDED_RECTANGLE
    assert isinstance(round_rect.manim_object, manim.RoundedRectangle)
    assert pytest.approx(round_rect.width, abs=1e-2) == 4.0


def test_shape_animate_highlight() -> None:
    """Verify animate_highlight returns valid Animation wrapping Indicate."""
    circle = Shape.circle()
    anim = circle.animate_highlight(color="#F59E0B", run_time=0.8)

    assert isinstance(anim, Animation)
    assert anim.run_time == 0.8
    assert isinstance(anim.to_manim(), manim.Indicate)
