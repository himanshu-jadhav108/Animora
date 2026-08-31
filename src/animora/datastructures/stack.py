"""Stack data structure component with LIFO push/pop animations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.vertical import VerticalLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class StackModel:
    """Pure Python LIFO Stack data model."""

    def __init__(self, initial_items: Sequence[Any] | None = None) -> None:
        self._items: list[Any] = list(initial_items or [])

    def push(self, item: Any) -> None:
        """Push an element onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Pop and return the top element from the stack."""
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return the top element without removing it."""
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def to_list(self) -> list[Any]:
        return list(self._items)


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class Stack(Component):
    """Visual Stack data structure component with vertical LIFO operations.

    Example:
    ```python
    stack = Stack([10, 20, 30])
    scene.play(stack.animate_push(40))
    scene.play(stack.animate_pop())
    ```
    """

    def __init__(
        self,
        items: Sequence[Any] | None = None,
        *,
        item_width: float = 2.0,
        item_height: float = 0.6,
        spacing: float = 0.1,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = StackModel(items)
        self._item_width = float(item_width)
        self._item_height = float(item_height)
        self._spacing = float(spacing)

        self._item_groups: list[Group] = []
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> StackModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Build stack elements vertically from bottom to top."""
        active_theme = get_active_theme()
        self._item_groups = []

        for val in self._model.to_list():
            box = Shape.rounded_rectangle(
                width=self._item_width,
                height=self._item_height,
                corner_radius=0.08,
                fill_color=active_theme.colors.primary,
                fill_opacity=0.85,
                stroke_color=active_theme.colors.border,
                stroke_width=active_theme.strokes.thin,
            )
            txt = Text(str(val), font_size=active_theme.typography.font_size_sm, color="#FFFFFF")
            self._item_groups.append(Group(box, txt))

        # Arrange items vertically (reversed so bottom is bottom, top is top)
        if self._item_groups:
            # We arrange top to bottom: reversed list
            rev_items = list(reversed(self._item_groups))
            container = Group(*rev_items)
            container.arrange(VerticalLayout(spacing=self._spacing, center_origin=True))
            return container.manim_object

        return manim.VGroup()

    def animate_push(self, value: Any, run_time: float | None = None) -> Animation:
        """Push item to model and animate dropping into the top of the stack."""
        self._model.push(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        box = Shape.rounded_rectangle(
            width=self._item_width,
            height=self._item_height,
            corner_radius=0.08,
            fill_color=active_theme.colors.secondary,
            fill_opacity=0.9,
            stroke_color=active_theme.colors.border,
        )
        txt = Text(str(value), font_size=active_theme.typography.font_size_sm, color="#FFFFFF")
        new_grp = Group(box, txt)

        # Calculate position directly above the current top
        if self._item_groups:
            top_center = self._item_groups[-1].center
            target_pos = [top_center[0], top_center[1] + self._item_height + self._spacing, 0.0]
        else:
            target_pos = list(self.center)

        start_pos = [target_pos[0], target_pos[1] + 2.0, 0.0]
        new_grp.move_to(start_pos)
        self._item_groups.append(new_grp)

        return Animation(
            component=new_grp,
            manim_animation=new_grp.manim_object.animate.move_to(target_pos),
            run_time=duration,
            name=f"push({value})",
        )

    def animate_pop(self, run_time: float | None = None) -> Animation:
        """Pop item from model and animate flying out of the stack."""
        popped_val = self._model.pop()
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        top_grp = self._item_groups.pop()
        target_pos = [top_grp.center[0], top_grp.center[1] + 2.0, 0.0]

        return Animation(
            component=top_grp,
            manim_animation=manim.AnimationGroup(
                top_grp.manim_object.animate.move_to(target_pos),
                manim.FadeOut(top_grp.manim_object),
                run_time=duration,
            ),
            run_time=duration,
            name=f"pop() -> {popped_val}",
        )

    def animate_peek(self, run_time: float | None = None) -> Animation:
        """Highlight the top item."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.fast
        top_grp = self._item_groups[-1]
        return Animation(
            component=top_grp,
            manim_animation=manim.Indicate(top_grp.manim_object, color=active_theme.colors.accent),
            run_time=duration,
            name="peek()",
        )


__all__ = [
    "Stack",
    "StackModel",
]
