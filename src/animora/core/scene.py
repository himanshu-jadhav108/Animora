"""Scene abstraction for Animora, extending Manim's Scene engine."""

from __future__ import annotations

from typing import Any

import manim

from animora.core.animation import Animation
from animora.core.component import Component


class Scene(manim.Scene):  # type: ignore[misc]
    """High-level Scene for Animora animations.

    Inherits from Manim's Scene while providing first-class support for
    Animora Component instances, high-level Animation bridges, and automatic
    unwrapping to underlying Manim vector primitives.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._registered_components: list[Component] = []

    def add(self, *items: Component | manim.Mobject) -> None:
        """Add components or native Manim mobjects to the scene."""
        mobjects_to_add: list[manim.Mobject] = []
        for item in items:
            if isinstance(item, Component):
                self._registered_components.append(item)
                mobjects_to_add.append(item.manim_object)
            else:
                mobjects_to_add.append(item)
        super().add(*mobjects_to_add)

    def remove(self, *items: Component | manim.Mobject) -> None:
        """Remove components or native Manim mobjects from the scene."""
        mobjects_to_remove: list[manim.Mobject] = []
        for item in items:
            if isinstance(item, Component):
                if item in self._registered_components:
                    self._registered_components.remove(item)
                mobjects_to_remove.append(item.manim_object)
            else:
                mobjects_to_remove.append(item)
        super().remove(*mobjects_to_remove)

    def play(
        self,
        *animations_or_components: Animation | Component | manim.Animation,
        **kwargs: Any,
    ) -> None:
        """Play one or more animations, Animora components, or Manim transforms.

        Accepts:
        - Animora Animation objects (unwrapped via .to_manim())
        - Animora Component objects (auto-plays .animate_fade_in())
        - Raw Manim Animation objects (e.g. Rotate, Transform, Wiggle)
        """
        manim_animations: list[manim.Animation] = []
        for item in animations_or_components:
            if isinstance(item, Animation):
                manim_animations.append(item.to_manim())
            elif isinstance(item, Component):
                # Auto-play fade in for bare components passed to play()
                anim = item.animate_fade_in()
                manim_animations.append(anim.to_manim())
            elif isinstance(item, manim.Animation):
                manim_animations.append(item)
            else:
                raise TypeError(
                    f"Unsupported item passed to Scene.play(): {type(item)}. "
                    "Expected Animora Animation, Component, or Manim Animation."
                )
        super().play(*manim_animations, **kwargs)


__all__ = [
    "Scene",
]
