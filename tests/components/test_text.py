"""Unit tests for the Text primitive component."""

from __future__ import annotations

import manim
import pytest

from animora.components.text import Text
from animora.core.animation import Animation


def test_text_initialization() -> None:
    """Verify Text construction, properties, and mobject creation."""
    txt = Text("Binary Tree", font_size=40, color="#38BDF8")

    assert txt.text == "Binary Tree"
    assert txt.config.font_size == 40
    assert txt.config.color == "#38BDF8"
    assert isinstance(txt.manim_object, manim.Text)


def test_text_set_text() -> None:
    """Verify set_text mutates string and rebuilds internal mobject at center."""
    txt = Text("Initial")
    txt.move_to([2.0, 1.0, 0.0])
    old_mob = txt.manim_object

    txt.set_text("Updated")
    assert txt.text == "Updated"
    assert txt.manim_object is not old_mob
    assert pytest.approx(txt.center[0], abs=1e-2) == 2.0
    assert pytest.approx(txt.center[1], abs=1e-2) == 1.0


def test_text_animate_transform_text() -> None:
    """Verify animate_transform_text produces valid Animation."""
    txt = Text("Before")
    anim = txt.animate_transform_text("After", run_time=1.2)

    assert isinstance(anim, Animation)
    assert anim.run_time == 1.2
    assert txt.text == "After"
    assert isinstance(anim.to_manim(), manim.Transform)
