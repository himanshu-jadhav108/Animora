"""Named animation timing and easing presets for Animora.

Builds on top of Animora's core Theme timing tokens to provide semantic,
ready-to-use animation pacing profiles (e.g. SNAPPY, SMOOTH, CINEMATIC, EDUCATIONAL).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import manim

if TYPE_CHECKING:
    from animora.theme.theme import Theme


@dataclass(frozen=True)
class TimingPreset:
    """A semantic animation timing profile bundling duration and easing curve.

    Attributes:
        name: Identifier for the preset.
        duration: Default runtime duration in seconds.
        rate_func: Manim rate function defining the easing trajectory.
        description: Pedagogical or visual intent of this preset.
    """

    name: str
    duration: float
    rate_func: Callable[[float], float]
    description: str = ""

    def resolve_duration(self, theme: Theme | None = None) -> float:
        """Resolve concrete duration, optionally scaling from an active theme."""
        return self.duration

    def apply_to_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """Apply preset duration and rate_func to an animation kwargs dict if not set."""
        result = dict(kwargs)
        if "run_time" not in result or result["run_time"] is None:
            result["run_time"] = self.duration
        if "rate_func" not in result or result["rate_func"] is None:
            result["rate_func"] = self.rate_func
        return result


# -----------------------------------------------------------------------------
# Canonical Named Presets
# -----------------------------------------------------------------------------

SNAPPY = TimingPreset(
    name="snappy",
    duration=0.35,
    rate_func=manim.rush_from,
    description="Fast, crisp transitions for rapid state progression.",
)

SMOOTH = TimingPreset(
    name="smooth",
    duration=0.8,
    rate_func=manim.smooth,
    description="Balanced, natural ease-in-out movement for general UI and shapes.",
)

CINEMATIC = TimingPreset(
    name="cinematic",
    duration=1.8,
    rate_func=manim.slow_into,
    description="Deliberate, graceful motion for hero reveals and wide camera pans.",
)

PLAYFUL = TimingPreset(
    name="playful",
    duration=0.6,
    rate_func=manim.there_and_back_with_pause,
    description="Springy, energetic trajectory for pedagogical emphasis and callouts.",
)

EDUCATIONAL = TimingPreset(
    name="educational",
    duration=1.4,
    rate_func=manim.smooth,
    description="Paced, steady demonstration timing suited for narrated tutorials.",
)

SLOW_MO = TimingPreset(
    name="slow_mo",
    duration=2.5,
    rate_func=manim.smooth,
    description="High-detail slow motion for dissecting intricate algorithmic mutations.",
)

PRESETS: dict[str, TimingPreset] = {
    "snappy": SNAPPY,
    "smooth": SMOOTH,
    "cinematic": CINEMATIC,
    "playful": PLAYFUL,
    "educational": EDUCATIONAL,
    "slow_mo": SLOW_MO,
}


def get_timing_preset(name_or_preset: str | TimingPreset) -> TimingPreset:
    """Retrieve a TimingPreset by name or validate an existing TimingPreset instance."""
    if isinstance(name_or_preset, TimingPreset):
        return name_or_preset
    key = str(name_or_preset).strip().lower().replace("-", "_")
    if key in PRESETS:
        return PRESETS[key]
    raise KeyError(
        f"Unknown timing preset '{name_or_preset}'. Available presets: {list(PRESETS.keys())}"
    )


__all__ = [
    "CINEMATIC",
    "EDUCATIONAL",
    "PLAYFUL",
    "PRESETS",
    "SLOW_MO",
    "SMOOTH",
    "SNAPPY",
    "TimingPreset",
    "get_timing_preset",
]
