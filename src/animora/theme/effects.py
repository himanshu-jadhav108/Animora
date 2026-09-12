"""Composable Effects Engine and Material System for Animora.

Implements the decoupled Effect Strategy pattern operating on visual components
using theme design tokens via pure 2D CPU Cairo animation compositions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import manim

from animora.core.animation import Animation
from animora.core.component import Component
from animora.theme.builtin import Cyberpunk, ModernDark, Monokai, PaperLight
from animora.theme.context import get_active_theme
from animora.theme.theme import (
    AnimationTiming,
    ColorPalette,
    CornerRadius,
    SpacingScale,
    StrokeScale,
    Theme,
    Typography,
)

if TYPE_CHECKING:
    pass

# -----------------------------------------------------------------------------
# 1. Creative Prototype Theme: Aurora (Polar Emerald / Electric Teal)
# -----------------------------------------------------------------------------
Aurora = Theme(
    name="aurora",
    colors=ColorPalette(
        primary="#38EF7D",  # Emerald Mint
        secondary="#11998E",  # Deep Teal
        accent="#00F0FF",  # Electric Cyan
        background="#0B132B",  # Polar Night
        surface="#1C2541",  # Northern Ice
        text="#F0FDF4",  # Ice White
        text_muted="#6EE7B7",  # Pale Jade
        border="#11998E",  # Aurora Teal
        success="#38EF7D",
        warning="#FCD34D",
        error="#F87171",
    ),
    typography=Typography(
        font_family=None,
        font_size_xs=18.0,
        font_size_sm=24.0,
        font_size_md=32.0,
        font_size_lg=40.0,
        font_size_xl=48.0,
        line_spacing=1.0,
    ),
    spacing=SpacingScale(xs=0.1, sm=0.25, md=0.5, lg=1.0, xl=2.0),
    strokes=StrokeScale(thin=1.0, regular=2.5, thick=4.0),
    corner_radius=CornerRadius(none=0.0, sm=0.1, md=0.2, lg=0.3, full=0.6),
    timing=AnimationTiming(fast=0.35, normal=0.9, slow=1.8),
)

THEMES_MAP: dict[str, Theme] = {
    "modern_dark": ModernDark,
    "moderndark": ModernDark,
    "cyberpunk": Cyberpunk,
    "paper_light": PaperLight,
    "paperlight": PaperLight,
    "monokai": Monokai,
    "aurora": Aurora,
}


# -----------------------------------------------------------------------------
# 2. Base Effect & Registry
# -----------------------------------------------------------------------------
class BaseEffect(ABC):
    """Abstract base class for all composable visual animation effects."""

    name: str

    @abstractmethod
    def build_animation(
        self,
        component: Component,
        theme: Theme,
        run_time: float,
        **kwargs: Any,
    ) -> manim.Animation:
        """Construct the Manim Animation for the target component."""
        pass


EFFECTS_REGISTRY: dict[str, BaseEffect] = {}


def register_effect(name: str) -> Callable[[type[BaseEffect]], type[BaseEffect]]:
    """Decorator to register an effect in the global EFFECTS_REGISTRY."""

    def decorator(cls: type[BaseEffect]) -> type[BaseEffect]:
        inst = cls()
        inst.name = name.lower()
        EFFECTS_REGISTRY[inst.name] = inst
        return cls

    return decorator


def get_effect(name: str) -> BaseEffect:
    """Retrieve registered effect by name."""
    normalized = name.lower().strip()
    if normalized not in EFFECTS_REGISTRY:
        raise KeyError(
            f"Effect '{name}' not found. Available effects: {list(EFFECTS_REGISTRY.keys())}"
        )
    return EFFECTS_REGISTRY[normalized]


# -----------------------------------------------------------------------------
# 3. Concrete Cairo CPU Effects
# -----------------------------------------------------------------------------
@register_effect("gradient_reveal")
class GradientRevealEffect(BaseEffect):
    """Staggered sub-character / sub-element chromatic reveal effect."""

    def build_animation(
        self,
        component: Component,
        theme: Theme,
        run_time: float,
        **kwargs: Any,
    ) -> manim.Animation:
        mob = component.manim_object
        submobjects = list(mob.submobjects)

        # Apply multi-tone palette gradient across sub-elements
        palette = [theme.colors.primary, theme.colors.accent, theme.colors.secondary]
        if submobjects:
            num = len(submobjects)
            for idx, subm in enumerate(submobjects):
                color_idx = int((idx / max(num - 1, 1)) * (len(palette) - 1))
                subm.set_color(palette[color_idx])

            return manim.AnimationGroup(
                *[manim.FadeIn(subm, shift=manim.UP * 0.15) for subm in submobjects],
                lag_ratio=0.08,
                run_time=run_time,
            )
        else:
            mob.set_color(theme.colors.primary)
            return manim.FadeIn(mob, shift=manim.UP * 0.2, run_time=run_time)


@register_effect("glitch")
class GlitchEffect(BaseEffect):
    """Rapid discrete chromatic jitter and horizontal coordinate displacement."""

    def build_animation(
        self,
        component: Component,
        theme: Theme,
        run_time: float,
        **kwargs: Any,
    ) -> manim.Animation:
        mob = component.manim_object
        orig_color = theme.colors.text
        glitch_color = theme.colors.accent
        alt_color = theme.colors.primary

        step_time = run_time / 4.0
        anim_1 = mob.animate(run_time=step_time).shift([0.15, 0.0, 0.0]).set_color(glitch_color)
        anim_2 = mob.animate(run_time=step_time).shift([-0.25, 0.05, 0.0]).set_color(alt_color)
        anim_3 = mob.animate(run_time=step_time).shift([0.15, -0.05, 0.0]).set_color(glitch_color)
        anim_4 = mob.animate(run_time=step_time).shift([-0.05, 0.0, 0.0]).set_color(orig_color)

        return manim.Succession(anim_1, anim_2, anim_3, anim_4, run_time=run_time)


@register_effect("pulse_glow")
class PulseGlowEffect(BaseEffect):
    """High-contrast emphasis pulse with scale expansion and accent indication."""

    def build_animation(
        self,
        component: Component,
        theme: Theme,
        run_time: float,
        **kwargs: Any,
    ) -> manim.Animation:
        mob = component.manim_object
        glow_color = theme.colors.accent

        return manim.Indicate(
            mob,
            color=glow_color,
            scale_factor=1.12,
            run_time=run_time,
        )


# -----------------------------------------------------------------------------
# 4. Public API Entry Point
# -----------------------------------------------------------------------------
def apply_effect(
    component: Component,
    effect: str | BaseEffect,
    theme: Theme | str | None = None,
    run_time: float | None = None,
    **kwargs: Any,
) -> Animation:
    """Apply a composable visual effect to a component using theme tokens.

    Parameters:
        component: Target component to apply the effect to.
        effect: Name of registered effect or BaseEffect instance.
        theme: Theme or theme name string (defaults to get_active_theme()).
        run_time: Animation duration in seconds.

    Returns:
        Animora Animation wrapping the composite Manim animation.
    """
    # 1. Resolve Theme
    if isinstance(theme, str):
        normalized = theme.lower().strip()
        resolved_theme = THEMES_MAP[normalized] if normalized in THEMES_MAP else get_active_theme()
    elif isinstance(theme, Theme):
        resolved_theme = theme
    else:
        resolved_theme = get_active_theme()

    # 2. Resolve Effect
    if isinstance(effect, str):
        resolved_effect = get_effect(effect)
    elif isinstance(effect, BaseEffect):
        resolved_effect = effect
    else:
        raise TypeError(f"Expected effect name (str) or BaseEffect, got: {type(effect).__name__}")

    duration = run_time or resolved_theme.timing.normal
    manim_anim = resolved_effect.build_animation(
        component=component,
        theme=resolved_theme,
        run_time=duration,
        **kwargs,
    )

    return Animation(
        component=component,
        manim_animation=manim_anim,
        run_time=duration,
        name=f"apply_effect('{resolved_effect.name}')",
    )


__all__ = [
    "EFFECTS_REGISTRY",
    "Aurora",
    "BaseEffect",
    "GlitchEffect",
    "GradientRevealEffect",
    "PulseGlowEffect",
    "apply_effect",
    "get_effect",
    "register_effect",
]
