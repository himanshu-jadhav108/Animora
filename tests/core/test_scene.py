"""Unit tests for Animora Scene wrapper."""

from __future__ import annotations

import manim

from animora.components.label import Label
from animora.core.scene import Scene


def test_scene_add_and_remove_components() -> None:
    """Verify adding and removing Animora Component instances from Scene."""
    scene = Scene()
    label = Label("Hello")
    circle = manim.Circle()

    scene.add(label, circle)
    assert label in scene._registered_components
    assert label.manim_object in scene.mobjects
    assert circle in scene.mobjects

    scene.remove(label, circle)
    assert label not in scene._registered_components
    assert label.manim_object not in scene.mobjects
    assert circle not in scene.mobjects


def test_scene_play_accepts_animora_animation(monkeypatch: object) -> None:
    """Verify Scene.play correctly handles Animora Animation, Component, and Manim Animation."""
    scene = Scene()
    label = Label("Animora Scene")
    anim = label.animate_fade_in(run_time=1.0)

    # Verify that unwrap works without raising TypeErrors
    # We test play invocation by spying on super().play
    played_anims: list[manim.Animation] = []

    def mock_play(*args: manim.Animation, **kwargs: object) -> None:
        played_anims.extend(args)

    # Monkeypatch manim.Scene.play on scene instance
    scene.play = Scene.play.__get__(scene, Scene)  # type: ignore[method-assign]
    monkeypatch.setattr(manim.Scene, "play", mock_play)  # type: ignore[attr-defined]

    # 1. Play Animora Animation
    scene.play(anim)
    assert len(played_anims) == 1
    assert isinstance(played_anims[0], manim.Animation)

    # 2. Play bare Component (auto-converted to fade-in)
    scene.play(label)
    assert len(played_anims) == 2

    # 3. Play raw Manim Animation
    scene.play(manim.Rotate(label.manim_object))
    assert len(played_anims) == 3
