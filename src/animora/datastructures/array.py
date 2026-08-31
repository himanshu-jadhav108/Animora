"""Array data structure component with state-aware mutation animations."""

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
from animora.layout.horizontal import HorizontalLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class ArrayListModel:
    """Pure data representation for an Array/List supporting tracked state transitions."""

    def __init__(self, initial_values: Sequence[Any] | None = None) -> None:
        self._items: list[Any] = list(initial_values or [])

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._items[index] = value

    def to_list(self) -> list[Any]:
        """Return a snapshot list of the elements."""
        return list(self._items)

    def swap(self, i: int, j: int) -> None:
        """Swap elements at indices i and j."""
        self._items[i], self._items[j] = self._items[j], self._items[i]

    def insert(self, index: int, value: Any) -> None:
        """Insert value at the specified index, shifting trailing elements."""
        self._items.insert(index, value)

    def delete(self, index: int) -> Any:
        """Delete element at the specified index."""
        return self._items.pop(index)


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class Array(Component):
    """Visual Array data structure component.

    Renders an indexed linear sequence of cells with state-aware animation
    methods (swap, insert, delete, highlight).

    Example:
    ```python
    arr = Array([42, 17, 89, 5, 23])
    scene.play(arr.animate_swap(0, 3))
    scene.play(arr.animate_highlight(3, color="#10B981"))
    ```
    """

    def __init__(
        self,
        values: Sequence[Any] | None = None,
        *,
        cell_width: float = 1.0,
        cell_height: float = 1.0,
        spacing: float = 0.15,
        show_indices: bool = True,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = ArrayListModel(values)
        self._cell_width = float(cell_width)
        self._cell_height = float(cell_height)
        self._spacing = float(spacing)
        self._show_indices = show_indices

        self._cell_boxes: list[Shape] = []
        self._cell_labels: list[Text] = []
        self._index_labels: list[Text] = []
        self._cell_groups: list[Group] = []

        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> ArrayListModel:
        """The underlying pure Python ArrayListModel."""
        return self._model

    def __len__(self) -> int:
        return len(self._model)

    def __getitem__(self, index: int) -> Any:
        return self._model[index]

    def _build_mobject(self) -> manim.Mobject:
        """Construct the visual cells, values, and index labels arranged horizontally."""
        active_theme = get_active_theme()

        self._cell_boxes = []
        self._cell_labels = []
        self._index_labels = []
        self._cell_groups = []

        for _idx, val in enumerate(self._model.to_list()):
            box = Shape.rounded_rectangle(
                width=self._cell_width,
                height=self._cell_height,
                corner_radius=0.1,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.border,
                stroke_width=active_theme.strokes.thin,
            )
            txt = Text(
                str(val),
                font_size=active_theme.typography.font_size_md,
                color=active_theme.colors.text,
            )
            grp = Group(box, txt)
            self._cell_boxes.append(box)
            self._cell_labels.append(txt)
            self._cell_groups.append(grp)

        # Arrange all cell groups horizontally
        container = Group(*self._cell_groups)
        container.arrange(HorizontalLayout(spacing=self._spacing, center_origin=True))

        all_mobjects: list[manim.Mobject] = [container.manim_object]

        if self._show_indices:
            for idx, grp in enumerate(self._cell_groups):
                idx_lbl = Text(
                    f"[{idx}]",
                    font_size=active_theme.typography.font_size_xs,
                    color=active_theme.colors.text_muted,
                ).move_to([grp.center[0], grp.center[1] - (self._cell_height / 2.0) - 0.3, 0.0])
                self._index_labels.append(idx_lbl)
                all_mobjects.append(idx_lbl.manim_object)

        return manim.VGroup(*all_mobjects)

    # -------------------------------------------------------------------------
    # State-Aware Animation Methods
    # -------------------------------------------------------------------------
    def animate_swap(
        self,
        i: int,
        j: int,
        run_time: float | None = None,
    ) -> Animation:
        """Mutate underlying model and generate swap arc animation."""
        self._model.swap(i, j)

        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        grp_i = self._cell_groups[i]
        grp_j = self._cell_groups[j]
        pos_i = grp_i.center
        pos_j = grp_j.center

        # Swap references in visual list
        self._cell_groups[i], self._cell_groups[j] = self._cell_groups[j], self._cell_groups[i]
        self._cell_boxes[i], self._cell_boxes[j] = self._cell_boxes[j], self._cell_boxes[i]
        self._cell_labels[i], self._cell_labels[j] = self._cell_labels[j], self._cell_labels[i]

        anim_i = manim.ApplyMethod(grp_i.manim_object.move_to, pos_j, path_arc=manim.PI / 2.0)
        anim_j = manim.ApplyMethod(grp_j.manim_object.move_to, pos_i, path_arc=-manim.PI / 2.0)

        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(anim_i, anim_j, run_time=duration),
            run_time=duration,
            name=f"swap({i}, {j})",
        )

    def animate_highlight(
        self,
        index: int,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Highlight cell at given index."""
        active_theme = get_active_theme()
        highlight_color = color or active_theme.colors.accent
        duration = run_time or active_theme.timing.fast

        target_box = self._cell_boxes[index]
        return Animation(
            component=target_box,
            manim_animation=manim.Indicate(target_box.manim_object, color=highlight_color),
            run_time=duration,
            name=f"highlight({index})",
        )

    def animate_set(
        self,
        index: int,
        value: Any,
        run_time: float | None = None,
    ) -> Animation:
        """Update value at index and animate text transformation."""
        self._model[index] = value
        lbl = self._cell_labels[index]
        return lbl.animate_transform_text(str(value), run_time=run_time or 0.8)


__all__ = [
    "Array",
    "ArrayListModel",
]
