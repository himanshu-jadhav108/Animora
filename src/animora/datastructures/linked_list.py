"""LinkedList data structure component with animated pointer transitions."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim

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


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class ListNode:
    """Node in a singly linked list."""

    def __init__(self, value: Any, next_node: ListNode | None = None) -> None:
        self.value: Any = value
        self.next: ListNode | None = next_node


class LinkedListModel:
    """Pure Python Singly-Linked List data model."""

    def __init__(self, initial_values: Sequence[Any] | None = None) -> None:
        self.head: ListNode | None = None
        for val in initial_values or []:
            self.insert_tail(val)

    def to_list(self) -> list[Any]:
        """Convert linked list nodes to a flat Python list."""
        result: list[Any] = []
        curr = self.head
        while curr is not None:
            result.append(curr.value)
            curr = curr.next
        return result

    def insert_head(self, value: Any) -> None:
        """Insert value at head of list."""
        new_node = ListNode(value, self.head)
        self.head = new_node

    def insert_tail(self, value: Any) -> None:
        """Insert value at tail of list."""
        new_node = ListNode(value)
        if self.head is None:
            self.head = new_node
            return
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node

    def delete(self, value: Any) -> bool:
        """Delete first node containing value. Return True if deleted."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True

        curr = self.head
        while curr.next is not None and curr.next.value != value:
            curr = curr.next

        if curr.next is not None:
            curr.next = curr.next.next
            return True
        return False

    def search(self, value: Any) -> int:
        """Return index of node with value, or -1 if not found."""
        curr = self.head
        idx = 0
        while curr is not None:
            if curr.value == value:
                return idx
            curr = curr.next
            idx += 1
        return -1


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class LinkedList(Component):
    """Visual Singly-Linked List data structure component.

    Renders value nodes, pointer arrows, and NULL indicator, providing
    visualized pointer modifications.

    Example:
    ```python
    ll = LinkedList([10, 20, 30])
    scene.play(ll.animate_insert_tail(40))
    ```
    """

    def __init__(
        self,
        values: Sequence[Any] | None = None,
        *,
        node_radius: float = 0.45,
        node_spacing: float = 1.6,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = LinkedListModel(values)
        self._node_radius = float(node_radius)
        self._node_spacing = float(node_spacing)

        self._node_groups: list[Group] = []
        self._arrows: list[Arrow] = []
        self._null_text: Text | None = None

        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> LinkedListModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Construct nodes, pointer arrows, and NULL label horizontally."""
        active_theme = get_active_theme()

        self._node_groups = []
        self._arrows = []
        all_mobjects: list[manim.Mobject] = []

        values = self._model.to_list()
        n = len(values)

        # Position nodes centered horizontally
        start_x = -((n * self._node_spacing) / 2.0) + (self._node_spacing / 2.0) if n > 0 else 0.0

        for i, val in enumerate(values):
            x = start_x + (i * self._node_spacing)
            pos = [x, 0.0, 0.0]

            circle = Shape.circle(
                radius=self._node_radius,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.primary,
                stroke_width=active_theme.strokes.regular,
            ).move_to(pos)

            txt = Text(
                str(val),
                font_size=active_theme.typography.font_size_sm,
                color=active_theme.colors.text,
            ).move_to(pos)
            node_grp = Group(circle, txt)
            self._node_groups.append(node_grp)
            all_mobjects.append(node_grp.manim_object)

        # Connect nodes with arrows
        for i in range(len(self._node_groups) - 1):
            arrow = Arrow(
                start=self._node_groups[i],
                end=self._node_groups[i + 1],
                buff=self._node_radius + 0.1,
                stroke_color=active_theme.colors.border,
            )
            self._arrows.append(arrow)
            all_mobjects.append(arrow.manim_object)

        # NULL label at tail
        if self._node_groups:
            last_pos = self._node_groups[-1].center
            null_pos = [last_pos[0] + self._node_spacing, last_pos[1], 0.0]
            null_arrow = Arrow(
                start=last_pos,
                end=null_pos,
                buff=self._node_radius + 0.1,
                stroke_color=active_theme.colors.text_muted,
            )
            self._null_text = Text(
                "NULL",
                font_size=active_theme.typography.font_size_xs,
                color=active_theme.colors.text_muted,
            ).move_to([null_pos[0] + 0.3, null_pos[1], 0.0])

            all_mobjects.append(null_arrow.manim_object)
            all_mobjects.append(self._null_text.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_insert_tail(self, value: Any, run_time: float | None = None) -> Animation:
        """Insert value at tail and animate new node and pointer appearance."""
        self._model.insert_tail(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        # Visual node
        circle = Shape.circle(
            radius=self._node_radius,
            fill_color=active_theme.colors.secondary,
            fill_opacity=0.9,
            stroke_color=active_theme.colors.primary,
        )
        txt = Text(str(value), font_size=active_theme.typography.font_size_sm, color="#FFFFFF")
        new_grp = Group(circle, txt)

        if self._node_groups:
            last_center = self._node_groups[-1].center
            target_pos = [last_center[0] + self._node_spacing, last_center[1], 0.0]
            arrow = Arrow(start=self._node_groups[-1], end=target_pos, buff=self._node_radius + 0.1)
        else:
            target_pos = list(self.center)
            arrow = None

        new_grp.move_to(target_pos)
        self._node_groups.append(new_grp)

        animations: list[manim.Animation] = [manim.FadeIn(new_grp.manim_object, scale=0.5)]
        if arrow is not None:
            animations.append(manim.Create(arrow.manim_object))

        return Animation(
            component=new_grp,
            manim_animation=manim.AnimationGroup(*animations, run_time=duration),
            run_time=duration,
            name=f"insert_tail({value})",
        )


__all__ = [
    "LinkedList",
    "LinkedListModel",
    "ListNode",
]
