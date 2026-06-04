"""Queue data structure component with FIFO enqueue/dequeue animations."""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any, Sequence
import manim

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.horizontal import HorizontalLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class QueueModel:
    """Pure Python FIFO Queue data model backed by collections.deque."""

    def __init__(self, initial_items: Sequence[Any] | None = None) -> None:
        self._deque: deque[Any] = deque(initial_items or [])

    def enqueue(self, item: Any) -> None:
        """Add item to the rear of the queue."""
        self._deque.append(item)

    def dequeue(self) -> Any:
        """Remove and return the item at the front of the queue."""
        if not self._deque:
            raise IndexError("dequeue from empty queue")
        return self._deque.popleft()

    def peek(self) -> Any:
        """Return the front item without removing it."""
        if not self._deque:
            raise IndexError("peek from empty queue")
        return self._deque[0]

    def is_empty(self) -> bool:
        return len(self._deque) == 0

    def size(self) -> int:
        return len(self._deque)

    def to_list(self) -> list[Any]:
        return list(self._deque)


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class Queue(Component):
    """Visual Queue data structure component with FIFO enqueue and dequeue operations.

    Example:
    ```python
    queue = Queue([10, 20, 30])
    scene.play(queue.animate_enqueue(40))
    scene.play(queue.animate_dequeue())
    ```
    """

    def __init__(
        self,
        items: Sequence[Any] | None = None,
        *,
        item_width: float = 1.0,
        item_height: float = 1.0,
        spacing: float = 0.15,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = QueueModel(items)
        self._item_width = float(item_width)
        self._item_height = float(item_height)
        self._spacing = float(spacing)

        self._item_groups: list[Group] = []
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> QueueModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Build horizontal cells for queue elements."""
        active_theme = get_active_theme()
        self._item_groups = []

        for val in self._model.to_list():
            box = Shape.rounded_rectangle(
                width=self._item_width,
                height=self._item_height,
                corner_radius=0.1,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.primary,
                stroke_width=active_theme.strokes.thin,
            )
            txt = Text(str(val), font_size=active_theme.typography.font_size_sm, color=active_theme.colors.text)
            self._item_groups.append(Group(box, txt))

        container = Group(*self._item_groups)
        container.arrange(HorizontalLayout(spacing=self._spacing, center_origin=True))
        return container.manim_object

    def animate_enqueue(self, value: Any, run_time: float | None = None) -> Animation:
        """Enqueue item into model and animate sliding into the rear (right)."""
        self._model.enqueue(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        box = Shape.rounded_rectangle(
            width=self._item_width,
            height=self._item_height,
            corner_radius=0.1,
            fill_color=active_theme.colors.secondary,
            fill_opacity=0.9,
            stroke_color=active_theme.colors.primary,
        )
        txt = Text(str(value), font_size=active_theme.typography.font_size_sm, color="#FFFFFF")
        new_grp = Group(box, txt)

        if self._item_groups:
            rear_center = self._item_groups[-1].center
            target_pos = [rear_center[0] + self._item_width + self._spacing, rear_center[1], 0.0]
        else:
            target_pos = list(self.center)

        start_pos = [target_pos[0] + 2.0, target_pos[1], 0.0]
        new_grp.move_to(start_pos)
        self._item_groups.append(new_grp)

        return Animation(
            component=new_grp,
            manim_animation=new_grp.manim_object.animate.move_to(target_pos),
            run_time=duration,
            name=f"enqueue({value})",
        )

    def animate_dequeue(self, run_time: float | None = None) -> Animation:
        """Dequeue item from model and animate sliding out of the front (left)."""
        dequeued_val = self._model.dequeue()
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        front_grp = self._item_groups.pop(0)
        target_pos = [front_grp.center[0] - 2.0, front_grp.center[1], 0.0]

        return Animation(
            component=front_grp,
            manim_animation=manim.AnimationGroup(
                front_grp.manim_object.animate.move_to(target_pos),
                manim.FadeOut(front_grp.manim_object),
                run_time=duration,
            ),
            run_time=duration,
            name=f"dequeue() -> {dequeued_val}",
        )

    def animate_peek(self, run_time: float | None = None) -> Animation:
        """Highlight front item."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.fast
        front_grp = self._item_groups[0]
        return Animation(
            component=front_grp,
            manim_animation=manim.Indicate(front_grp.manim_object, color=active_theme.colors.accent),
            run_time=duration,
            name="peek()",
        )


__all__ = [
    "Queue",
    "QueueModel",
]
