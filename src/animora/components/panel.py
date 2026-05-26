"""Panel primitive component for framing and grouping visual elements with a background card."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence
import manim

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.component import Component
from animora.core.config import ComponentConfig

if TYPE_CHECKING:
    from typing_extensions import Self


class Panel(Component):
    """A framed card/panel container component with a styled background shape.

    Wraps child components or standalone content within a padded background card,
    optionally displaying a header title.

    Example:
    ```python
    code_text = Text("x = 42\ny = x * 2", font_size=24)
    panel = Panel(
        children=[code_text],
        title="Variables",
        padding=0.4,
        fill_color="#0F172A",
        stroke_color="#38BDF8",
    )
    ```
    """

    def __init__(
        self,
        *children: Component,
        title: str | Text | None = None,
        padding: float = 0.4,
        corner_radius: float = 0.2,
        fill_color: str | None = "#0F172A",
        fill_opacity: float = 0.9,
        stroke_color: str | None = "#38BDF8",
        stroke_width: float = 2.0,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        cfg = config or ComponentConfig(
            color=stroke_color or "#38BDF8",
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
        self._padding = float(padding)
        self._corner_radius = float(corner_radius)
        self._content_group = Group(*children)
        self._title_comp: Text | None = (
            Text(title, font_size=28, color=stroke_color)
            if isinstance(title, str)
            else title
        )
        self._bg_shape: Shape | None = None
        super().__init__(config=cfg, **kwargs)

    @property
    def content(self) -> Group:
        """The content group of child components."""
        return self._content_group

    @property
    def title(self) -> Text | None:
        """The header title component, if present."""
        return self._title_comp

    def _build_mobject(self) -> manim.Mobject:
        """Construct the composite background panel and position children."""
        content_items: list[Component] = []
        if self._title_comp is not None:
            content_items.append(self._title_comp)
        content_items.extend(self._content_group.children)

        # Calculate bounding dimensions of enclosed content
        if content_items:
            content_group = Group(*content_items)
            w = content_group.width + (2.0 * self._padding)
            h = content_group.height + (2.0 * self._padding)
            center = content_group.center
        else:
            w = 3.0
            h = 2.0
            center = [0.0, 0.0, 0.0]

        # Minimum sizing
        w = max(w, 2.0)
        h = max(h, 1.5)

        self._bg_shape = Shape.rounded_rectangle(
            width=w,
            height=h,
            corner_radius=self._corner_radius,
            fill_color=self.config.fill_color or "#0F172A",
            fill_opacity=self.config.fill_opacity,
            stroke_color=self.config.stroke_color or "#38BDF8",
            stroke_width=self.config.stroke_width,
        ).move_to(center)

        all_mobjects: list[manim.Mobject] = [self._bg_shape.manim_object]
        for item in content_items:
            all_mobjects.append(item.manim_object)

        return manim.VGroup(*all_mobjects)


__all__ = [
    "Panel",
]
