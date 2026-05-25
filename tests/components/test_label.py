"""Unit tests for the Label component."""

from __future__ import annotations

import manim
import pytest

from animora.components.label import Label
from animora.core.animation import Animation


def test_label_initialization() -> None:
    """Verify Label constructor, properties, and mobject construction."""
    label = Label("Hello Animora", font_size=32, color="#38BDF8")

    assert label.text == "Hello Animora"
    assert label.config.font_size == 32
    assert label.config.color == "#38BDF8"
    assert isinstance(label.manim_object, manim.Text)


def test_label_set_text() -> None:
    """Verify modifying text updates content and rebuilds internal mobject."""
    label = Label("Initial Text")
    label.move_to([1.0, 2.0, 0.0])
    old_mobject = label.manim_object

    label.set_text("Updated Text")
    assert label.text == "Updated Text"
    assert label.manim_object is not old_mobject
    assert isinstance(label.manim_object, manim.Text)
    # Center should be preserved
    assert pytest.approx(label.center[0], abs=1e-2) == 1.0
    assert pytest.approx(label.center[1], abs=1e-2) == 2.0


def test_label_animate_transform_text() -> None:
    """Verify animate_transform_text returns valid Animation instance."""
    label = Label("Count: 0")
    anim = label.animate_transform_text("Count: 1", run_time=1.5)

    assert isinstance(anim, Animation)
    assert anim.run_time == 1.5
    assert label.text == "Count: 1"
    manim_anim = anim.to_manim()
    assert isinstance(manim_anim, manim.Transform)
