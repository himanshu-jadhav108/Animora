"""Unit tests for the Arrow primitive component."""

from __future__ import annotations

import manim
import pytest

from animora.components.arrow import Arrow
from animora.components.shape import Shape
from animora.core.animation import Animation


def test_arrow_straight_construction() -> None:
    """Verify Arrow constructs Manim Arrow between endpoints."""
    node_a = Shape.circle(radius=0.4).move_to([-1.0, 0.0, 0.0])
    node_b = Shape.circle(radius=0.4).move_to([1.0, 0.0, 0.0])

    arrow = Arrow(start=node_a, end=node_b, stroke_color="#38BDF8")
    assert isinstance(arrow.manim_object, manim.Arrow)


def test_arrow_curved_construction() -> None:
    """Verify curved Arrow constructs Manim CurvedArrow."""
    arrow = Arrow(start=[0, 0, 0], end=[3, 0, 0], path_arc=1.0)
    assert isinstance(arrow.manim_object, manim.CurvedArrow)


def test_arrow_animate_highlight() -> None:
    """Verify animate_highlight returns valid Animation."""
    arrow = Arrow(start=[0, 0, 0], end=[1, 1, 0])
    anim = arrow.animate_highlight(color="#F59E0B", run_time=0.9)

    assert isinstance(anim, Animation)
    assert anim.run_time == 0.9
    assert isinstance(anim.to_manim(), manim.Indicate)
