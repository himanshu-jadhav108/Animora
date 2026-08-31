"""Animation abstraction bridging Animora semantic actions to Manim animations."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import manim

if TYPE_CHECKING:
    from animora.core.component import Component


class Animation:
    """High-level animation abstraction for Animora.

    Wraps and generates underlying Manim animation primitives, tracking
    timing, easing/rate functions, and target components.
    """

    def __init__(
        self,
        component: Component,
        manim_animation: manim.Animation | None = None,
        run_time: float = 1.0,
        rate_func: Callable[[float], float] | None = None,
        name: str = "custom_animation",
    ) -> None:
        self._component = component
        self._manim_animation = manim_animation
        self._run_time = float(run_time)
        self._rate_func = rate_func or manim.smooth
        self._name = name

    @property
    def component(self) -> Component:
        """The target Component being animated."""
        return self._component

    @property
    def run_time(self) -> float:
        """Duration of the animation in seconds."""
        return self._run_time

    @property
    def name(self) -> str:
        """Semantic name of the animation."""
        return self._name

    def to_manim(self) -> manim.Animation:
        """Produce or return the underlying Manim Animation instance."""
        if self._manim_animation is not None:
            # Apply run_time and rate_func if explicitly provided
            self._manim_animation.set_run_time(self._run_time)
            if self._rate_func is not None:
                self._manim_animation.rate_func = self._rate_func
            return self._manim_animation

        # Default fallback is Transform to current state
        return manim.FadeIn(
            self._component.manim_object,
            run_time=self._run_time,
            rate_func=self._rate_func,
        )

    def __repr__(self) -> str:
        return (
            f"<Animora.Animation '{self._name}' on {self._component} (run_time={self._run_time}s)>"
        )


__all__ = [
    "Animation",
]
