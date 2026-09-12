"""Annotation component for educational callouts, pointers, and explanations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.arrow import Arrow
from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class Annotation(Component):
    """An educational callout annotation attached to a target component or position.

    Composes a textual label (or framed callout card) with an optional directional
    pointer arrow directed toward the target element, styled with active theme tokens.

    Example:
    ```python
    node = Shape.circle(radius=0.5)
    ann = Annotation(node, text="Root Node", direction=manim.UP, buff=0.6, arrow=True)
    scene.play(ann.animate_create())
    ```
    """

    def __init__(
        self,
        target: Component | Sequence[float] | np.ndarray,
        text: str,
        *,
        direction: np.ndarray | Sequence[float] = manim.UP,
        buff: float = 0.6,
        arrow: bool = True,
        box: bool = False,
        color: str | None = None,
        font_size: float | None = None,
        box_padding: float | None = None,
        arrow_color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._target_ref = target
        self._text_content = str(text)
        self._direction = np.asarray(direction, dtype=float)
        dir_norm = np.linalg.norm(self._direction)
        if dir_norm > 1e-6:
            self._direction = self._direction / dir_norm
        else:
            self._direction = np.array([0.0, 1.0, 0.0])

        self._buff = float(buff)
        self._has_arrow = bool(arrow)
        self._has_box = bool(box)
        self._custom_color = color
        self._font_size = font_size
        self._box_padding = box_padding
        self._arrow_color = arrow_color

        self._content_component: Component | None = None
        self._arrow_component: Arrow | None = None

        super().__init__(config=config, **kwargs)

    @property
    def target(self) -> Component | Sequence[float] | np.ndarray:
        """The target component or coordinate point being annotated."""
        return self._target_ref

    @property
    def text(self) -> str:
        """The annotation text string."""
        return self._text_content

    @property
    def content_component(self) -> Component | None:
        """The label or card component displayed in the annotation."""
        _ = self.manim_object
        return self._content_component

    @property
    def arrow_component(self) -> Arrow | None:
        """The arrow component pointing to the target, if enabled."""
        _ = self.manim_object
        return self._arrow_component

    def _build_mobject(self) -> manim.Mobject:
        """Construct the callout text/box and connector arrow oriented toward the target."""
        active_theme = get_active_theme()

        # 1. Resolve target coordinates and mobject
        if isinstance(self._target_ref, Component):
            target_mob: manim.Mobject | None = self._target_ref.manim_object
            target_pos = self._target_ref.center
        else:
            target_mob = None
            target_pos = np.asarray(self._target_ref, dtype=float)

        text_color = self._custom_color or active_theme.colors.text
        text_size = (
            self._font_size if self._font_size is not None else active_theme.typography.font_size_sm
        )

        # 2. Build content (plain Text or bordered Box)
        label_text = Text(self._text_content, font_size=text_size, color=text_color)

        if self._has_box:
            pad = (
                float(self._box_padding)
                if self._box_padding is not None
                else active_theme.spacing.sm
            )
            box_w = max(label_text.width + (2.0 * pad), 0.8)
            box_h = max(label_text.height + (2.0 * pad), 0.5)

            card_shape = Shape.rounded_rectangle(
                width=box_w,
                height=box_h,
                corner_radius=active_theme.corner_radius.sm,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.95,
                stroke_color=self._custom_color or active_theme.colors.border,
                stroke_width=active_theme.strokes.thin,
            )
            content_grp = Group(card_shape, label_text)
            self._content_component = content_grp
        else:
            self._content_component = label_text

        # 3. Position content relative to target
        if target_mob is not None:
            self._content_component.next_to(target_mob, direction=self._direction, buff=self._buff)
        else:
            # Shift content center relative to target position
            offset_dist = self._buff + (
                self._content_component.height / 2.0
                if abs(self._direction[1]) > abs(self._direction[0])
                else self._content_component.width / 2.0
            )
            self._content_component.move_to(target_pos + (self._direction * offset_dist))

        all_mobjects: list[manim.Mobject] = [self._content_component.manim_object]

        # 4. Construct directional Arrow if requested
        if self._has_arrow:
            arrow_stroke_color = (
                self._arrow_color
                or self._custom_color
                or active_theme.colors.accent
                or active_theme.colors.primary
            )

            # Arrow points FROM annotation content TO target
            content_mob = self._content_component.manim_object
            if target_mob is not None:
                p_start = content_mob.get_critical_point(-self._direction)
                p_end = target_mob.get_critical_point(self._direction)
            else:
                p_start = content_mob.get_critical_point(-self._direction)
                p_end = target_pos

            # If start and end are sufficiently separated, construct the arrow
            dist = float(np.linalg.norm(p_end - p_start))
            if dist > 0.15:
                self._arrow_component = Arrow(
                    start=p_start,
                    end=p_end,
                    buff=0.06,
                    tip_length=min(0.2, dist * 0.4),
                    stroke_color=arrow_stroke_color,
                    stroke_width=active_theme.strokes.regular,
                )
                all_mobjects.append(self._arrow_component.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_create(self, run_time: float | None = None) -> Animation:
        """Animate entry transition for the annotation."""
        _ = self.manim_object
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        anims: list[manim.Animation] = []
        if self._content_component is not None:
            anims.append(manim.FadeIn(self._content_component.manim_object))
        if self._arrow_component is not None:
            anims.append(manim.Create(self._arrow_component.manim_object))

        if anims:
            composed = manim.AnimationGroup(*anims, lag_ratio=0.2, run_time=duration)
        else:
            composed = manim.FadeIn(self.manim_object, run_time=duration)

        return Animation(
            component=self,
            manim_animation=composed,
            run_time=duration,
            name=f"annotate('{self._text_content}')",
        )

    def animate_fade_in(self, run_time: float | None = None) -> Animation:
        """Fade in the annotation."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.fast
        return Animation(
            component=self,
            manim_animation=manim.FadeIn(self.manim_object),
            run_time=duration,
            name=f"fade_in_annotation('{self._text_content}')",
        )

    def animate_fade_out(self, run_time: float | None = None) -> Animation:
        """Fade out the annotation."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.fast
        return Animation(
            component=self,
            manim_animation=manim.FadeOut(self.manim_object),
            run_time=duration,
            name=f"fade_out_annotation('{self._text_content}')",
        )


__all__ = [
    "Annotation",
]
