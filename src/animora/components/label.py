"""Label primitive component for text display and typography."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
import manim

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig

if TYPE_CHECKING:
    from typing_extensions import Self


class Label(Component):
    """A high-level text label component.

    Provides declarative text rendering, font sizing, color styling, and
    text transformation animations built on top of Manim's Text mobject.

    Example:
    ```python
    label = Label("Hello, Animora!", font_size=40, color="#38BDF8")
    label.move_to([0, 2, 0])
    scene.play(label.animate_fade_in())
    ```
    """

    def __init__(
        self,
        text: str,
        *,
        font_size: float | None = None,
        color: str | None = None,
        font: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        cfg = config or ComponentConfig()
        if font_size is not None:
            cfg = cfg.merge(font_size=font_size)
        if color is not None:
            cfg = cfg.merge(color=color)
        if font is not None:
            cfg = cfg.merge(font_family=font)

        self._text_content: str = text
        super().__init__(config=cfg, **kwargs)

    @property
    def text(self) -> str:
        """The textual content of the label."""
        return self._text_content

    def set_text(self, new_text: str) -> Self:
        """Update the label text content and rebuild its visual representation."""
        self._text_content = new_text
        old_center = self.center
        self._mobject = self._build_mobject()
        self.move_to(old_center)
        return self

    def _build_mobject(self) -> manim.Mobject:
        """Construct the underlying Manim Text instance."""
        return manim.Text(
            self._text_content,
            font_size=self.config.font_size,
            color=self.config.color,
            font=self.config.font_family or "",
        )

    def animate_transform_text(
        self,
        new_text: str,
        run_time: float = 1.0,
    ) -> Animation:
        """Animate transitioning the label's text to a new string via Manim Transform."""
        target_mobject = manim.Text(
            new_text,
            font_size=self.config.font_size,
            color=self.config.color,
            font=self.config.font_family or "",
        ).move_to(self.manim_object)

        self._text_content = new_text

        return Animation(
            component=self,
            manim_animation=manim.Transform(self.manim_object, target_mobject),
            run_time=run_time,
            name=f"transform_text('{new_text}')",
        )


__all__ = [
    "Label",
]
