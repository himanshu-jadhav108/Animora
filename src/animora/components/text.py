"""Text primitive component for general typography and multi-line content."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
import manim

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


class Text(Component):
    """General-purpose styled text component for typography and titles.

    Supports multi-line text strings, custom font families, font sizing,
    colors, and text transform animations with active theme resolution.

    Example:
    ```python
    title = Text("Binary Search Trees", font_size=42, color="#38BDF8")
    title.move_to([0, 3, 0])
    scene.play(title.animate_fade_in())
    ```
    """

    def __init__(
        self,
        text: str,
        *,
        font_size: float | None = None,
        color: str | None = None,
        font: str | None = None,
        line_spacing: float = 1.0,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        active_theme = get_active_theme()
        cfg = config or ComponentConfig()
        resolved_cfg = cfg.merge(
            font_size=font_size if font_size is not None else active_theme.typography.font_size_md,
            color=color if color is not None else active_theme.colors.text,
            font_family=font if font is not None else active_theme.typography.font_family,
        ).resolve_with_theme(active_theme)

        self._text_content: str = text
        self._line_spacing: float = line_spacing
        super().__init__(config=resolved_cfg, **kwargs)

    @property
    def text(self) -> str:
        """The textual string displayed by the component."""
        return self._text_content

    def set_text(self, new_text: str) -> Self:
        """Update text string and re-render visual mobject at current center."""
        self._text_content = new_text
        old_center = self.center
        self._mobject = self._build_mobject()
        self.move_to(old_center)
        return self

    def _build_mobject(self) -> manim.Mobject:
        """Build underlying Manim Text instance."""
        return manim.Text(
            self._text_content,
            font_size=self.config.font_size,
            color=self.config.color,
            font=self.config.font_family or "",
            line_spacing=self._line_spacing,
        )

    def animate_transform_text(
        self,
        new_text: str,
        run_time: float = 1.0,
    ) -> Animation:
        """Animate transitioning this text to a new string via Manim Transform."""
        target_mobject = manim.Text(
            new_text,
            font_size=self.config.font_size,
            color=self.config.color,
            font=self.config.font_family or "",
            line_spacing=self._line_spacing,
        ).move_to(self.manim_object)

        self._text_content = new_text

        return Animation(
            component=self,
            manim_animation=manim.Transform(self.manim_object, target_mobject),
            run_time=run_time,
            name=f"transform_text('{new_text}')",
        )


__all__ = [
    "Text",
]
