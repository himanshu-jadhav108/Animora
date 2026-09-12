"""Unit tests for the Effects Engine prototype and theme composition."""

from __future__ import annotations

from typing import Any

import manim
import pytest

from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.scene import Scene
from animora.theme.builtin import Cyberpunk, ModernDark
from animora.theme.effects import (
    Aurora,
    GlitchEffect,
    GradientRevealEffect,
    PulseGlowEffect,
    apply_effect,
    get_effect,
)


def test_registered_effects() -> None:
    """Verify built-in effects are properly registered in the engine."""
    assert isinstance(get_effect("gradient_reveal"), GradientRevealEffect)
    assert isinstance(get_effect("glitch"), GlitchEffect)
    assert isinstance(get_effect("pulse_glow"), PulseGlowEffect)

    with pytest.raises(KeyError):
        get_effect("nonexistent_effect")


def test_effects_produce_valid_animations() -> None:
    """Verify each effect produces a valid Animora Animation object."""
    txt = Text("Test Title", font_size=32)

    for effect_name in ["gradient_reveal", "glitch", "pulse_glow"]:
        anim = apply_effect(txt, effect=effect_name, run_time=1.0)
        assert isinstance(anim, Animation)
        assert anim.component is txt
        assert anim.run_time == 1.0
        assert anim.to_manim() is not None


@pytest.mark.parametrize("theme", [ModernDark, Cyberpunk, Aurora, "cyberpunk", "aurora"])
def test_effects_across_multiple_themes(theme: Any) -> None:
    """Verify the same effect operates across distinct themes without coupling."""
    txt = Text("Multi-Theme Verification")
    anim = apply_effect(txt, effect="gradient_reveal", theme=theme, run_time=0.8)

    assert isinstance(anim, Animation)
    assert anim.to_manim() is not None


def test_component_apply_effect_convenience() -> None:
    """Verify Component.apply_effect() delegates smoothly to the effects engine."""
    txt = Text("Heading")
    anim = txt.apply_effect(effect="glitch", theme=Aurora, run_time=0.5)

    assert isinstance(anim, Animation)
    assert anim.component is txt
    assert anim.run_time == 0.5


def test_effects_dry_run_scene_render() -> None:
    """Verify end-to-end rendering of effects in Scene with CPU Cairo renderer."""

    class EffectsDemoScene(Scene):
        def construct(self) -> None:
            t1 = Text("Aurora Title", font_size=36).move_to([0.0, 1.0, 0.0])
            self.play(t1.apply_effect("gradient_reveal", theme=Aurora, run_time=0.5))

            t2 = Text("Cyberpunk Glitch", font_size=28).move_to([0.0, -1.0, 0.0])
            self.play(t2.apply_effect("glitch", theme=Cyberpunk, run_time=0.4))
            self.play(t2.apply_effect("pulse_glow", run_time=0.3))
            self.wait(0.1)

    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        scene = EffectsDemoScene()
        scene.render()
        assert len(scene.mobjects) >= 2
