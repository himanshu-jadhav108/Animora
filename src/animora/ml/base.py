"""Base classes and tracing primitives for machine learning visualizations."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme


@dataclass(frozen=True)
class MLTraceStep:
    """A single recorded event in an ML optimization or inference trace."""

    step_index: int
    name: str
    values: dict[str, Any] = field(default_factory=dict)
    description: str = ""


class MLTrace:
    """Chronological record of mathematical steps in an ML algorithm.

    Enables independent validation of computational models prior to rendering.
    """

    def __init__(self, steps: Sequence[MLTraceStep] | None = None) -> None:
        self._steps: list[MLTraceStep] = list(steps or [])

    def record(
        self,
        name: str,
        description: str = "",
        **values: Any,
    ) -> MLTraceStep:
        """Record an atomic mathematical step."""
        step = MLTraceStep(
            step_index=len(self._steps),
            name=name,
            values=dict(values),
            description=description,
        )
        self._steps.append(step)
        return step

    def __len__(self) -> int:
        return len(self._steps)

    def __iter__(self) -> Iterator[MLTraceStep]:
        return iter(self._steps)

    def __getitem__(self, index: int) -> MLTraceStep:
        return self._steps[index]

    @property
    def steps(self) -> list[MLTraceStep]:
        return list(self._steps)


class MLComponent(Component):
    """Abstract base class for all AI/Machine Learning visual components.

    Enforces the One-Call API contract and theme token integration.
    """

    def __init__(
        self,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(config=config, **kwargs)

    def animate_create(self, run_time: float | None = None) -> Animation:
        """Construct the visual component in the scene."""
        import manim

        active_theme = get_active_theme()
        duration = run_time if run_time is not None else active_theme.timing.normal
        return Animation(
            component=self,
            manim_animation=manim.Create(self.manim_object),
            run_time=duration,
            name="create_ml_component",
        )

    def animate_fade_in(self, run_time: float | None = None) -> Animation:
        """Fade in the visual component in the scene."""
        import manim

        active_theme = get_active_theme()
        duration = run_time if run_time is not None else active_theme.timing.fast
        return Animation(
            component=self,
            manim_animation=manim.FadeIn(self.manim_object),
            run_time=duration,
            name="fade_in_ml_component",
        )


__all__ = [
    "MLComponent",
    "MLTrace",
    "MLTraceStep",
]
