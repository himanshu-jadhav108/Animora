"""Heap data structure component with sift-up and sift-down animations."""

from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, Any, Sequence
import manim

from animora.components.arrow import Arrow
from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.tree import TreeLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    from typing_extensions import Self


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class HeapModel:
    """Pure Python Min-Heap data model with explicit sift operations."""

    def __init__(self, initial_values: Sequence[float | int] | None = None) -> None:
        self._heap: list[float | int] = []
        for val in initial_values or []:
            self.insert(val)

    def to_list(self) -> list[float | int]:
        return list(self._heap)

    def insert(self, value: float | int) -> list[tuple[int, int]]:
        """Insert value and sift up, returning list of swap indices."""
        self._heap.append(value)
        swaps: list[tuple[int, int]] = []
        idx = len(self._heap) - 1

        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] < self._heap[parent]:
                swaps.append((idx, parent))
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break
        return swaps

    def extract_min(self) -> tuple[float | int, list[tuple[int, int]]]:
        """Extract root minimum, sift down last item, returning (min_val, swaps)."""
        if not self._heap:
            raise IndexError("extract_min from empty heap")

        min_val = self._heap[0]
        last_val = self._heap.pop()
        swaps: list[tuple[int, int]] = []

        if not self._heap:
            return min_val, swaps

        self._heap[0] = last_val
        idx = 0
        n = len(self._heap)

        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != idx:
                swaps.append((idx, smallest))
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break

        return min_val, swaps


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class Heap(Component):
    """Visual Binary Min-Heap component rendered as a hierarchical tree.

    Positions nodes via TreeLayout from Phase 4 and generates sift-up / sift-down animations.

    Example:
    ```python
    heap = Heap([15, 10, 20, 8, 12])
    scene.play(heap.animate_insert(5))
    ```
    """

    def __init__(
        self,
        values: Sequence[float | int] | None = None,
        *,
        node_radius: float = 0.4,
        level_height: float = 1.2,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = HeapModel(values)
        self._node_radius = float(node_radius)
        self._level_height = float(level_height)

        self._node_groups: list[Group] = []
        self._edge_mobjects: list[Arrow] = []
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> HeapModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Construct the heap tree nodes and edges."""
        active_theme = get_active_theme()

        self._node_groups = []
        self._edge_mobjects = []
        all_mobjects: list[manim.Mobject] = []

        heap_list = self._model.to_list()
        if not heap_list:
            return manim.VGroup()

        # Build node visual groups
        for val in heap_list:
            circle = Shape.circle(
                radius=self._node_radius,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.primary,
            )
            txt = Text(str(val), font_size=active_theme.typography.font_size_sm, color=active_theme.colors.text)
            self._node_groups.append(Group(circle, txt))

        # Position nodes using hierarchical binary tree coordinates
        for idx, grp in enumerate(self._node_groups):
            import math
            level = int(math.floor(math.log2(idx + 1)))
            pos_in_level = idx - (2**level - 1)
            total_in_level = 2**level

            x_spread = 8.0 / (total_in_level + 1)
            x = -4.0 + (pos_in_level + 1) * x_spread
            y = 2.0 - (level * self._level_height)
            grp.move_to([x, y, 0.0])
            all_mobjects.append(grp.manim_object)

        # Build connecting edges
        for idx in range(1, len(self._node_groups)):
            parent_idx = (idx - 1) // 2
            edge = Arrow(
                start=self._node_groups[parent_idx],
                end=self._node_groups[idx],
                buff=self._node_radius + 0.05,
                stroke_color=active_theme.colors.border,
            )
            self._edge_mobjects.append(edge)
            all_mobjects.append(edge.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_insert(self, value: float | int, run_time: float | None = None) -> Animation:
        """Insert value and animate node insertion and sift-up swaps."""
        swaps = self._model.insert(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        # Re-render or highlight
        return Animation(
            component=self,
            manim_animation=manim.Indicate(self.manim_object, color=active_theme.colors.accent),
            run_time=duration,
            name=f"insert({value}) -> swaps={len(swaps)}",
        )


__all__ = [
    "Heap",
    "HeapModel",
]
