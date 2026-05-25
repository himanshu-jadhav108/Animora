"""Unit tests for the Animation abstraction bridge."""

from __future__ import annotations

import manim
from animora.components.label import Label
from animora.core.animation import Animation


def test_animation_initialization() -> None:
    """Verify Animation properties and wrapper mechanics."""
    label = Label("Test")
    anim = Animation(component=label, run_time=2.5, name="fade_test")

    assert anim.component is label
    assert anim.run_time == 2.5
    assert anim.name == "fade_test"

    manim_anim = anim.to_manim()
    assert isinstance(manim_anim, manim.Animation)
    assert manim_anim.run_time == 2.5


def test_animation_with_explicit_manim_animation() -> None:
    """Verify Animation wraps custom Manim animation instances."""
    label = Label("Custom")
    raw_anim = manim.FadeOut(label.manim_object)
    anim = Animation(component=label, manim_animation=raw_anim, run_time=1.8)

    unwrapped = anim.to_manim()
    assert unwrapped is raw_anim
    assert unwrapped.run_time == 1.8
