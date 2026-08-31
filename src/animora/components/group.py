"""Group composite component for bundling multiple components into a single unit."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

import manim

from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.base import BaseLayout, LayoutItem

if TYPE_CHECKING:
    from typing_extensions import Self


class Group(Component):
    """A composite container component for grouping multiple components.

    Allows treating a collection of components as a single structural unit,
    supporting collective transformations, animations, indexing, and automatic
    layout arrangement.

    Example:
    ```python
    node1 = Shape.circle(radius=0.5)
    node2 = Shape.circle(radius=0.5)
    group = Group(node1, node2)
    group.arrange(HorizontalLayout(spacing=0.5))
    ```
    """

    def __init__(
        self,
        *children: Component,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._group_children: list[Component] = list(children)
        super().__init__(config=config, **kwargs)

    @property
    def children(self) -> list[Component]:
        """List of child components in this group."""
        return list(self._group_children)

    def add(self, *children: Component) -> Self:
        """Add one or more child components to the group."""
        for child in children:
            if child not in self._group_children:
                self._group_children.append(child)
                if self._mobject is not None:
                    self._mobject.add(child.manim_object)
        return self

    def remove(self, *children: Component) -> Self:
        """Remove one or more child components from the group."""
        for child in children:
            if child in self._group_children:
                self._group_children.remove(child)
                if self._mobject is not None:
                    self._mobject.remove(child.manim_object)
        return self

    def arrange(
        self,
        layout: BaseLayout,
        **kwargs: Any,
    ) -> Self:
        """Automatically arrange child components according to a layout solver.

        Translates children into abstract LayoutItems, solves for 3D coordinates,
        and applies positions to each child component.
        """
        if not self._group_children:
            return self

        items = [
            LayoutItem(
                id=str(idx),
                width=child.width,
                height=child.height,
                depth=child.depth,
            )
            for idx, child in enumerate(self._group_children)
        ]

        result = layout.solve(items, **kwargs)

        for idx, child in enumerate(self._group_children):
            item_id = str(idx)
            if item_id in result.positions:
                pos = result.positions[item_id]
                child.move_to(pos)

        # Invalidate cached group mobject to reflect new child positions
        self._mobject = self._build_mobject()
        return self

    def _build_mobject(self) -> manim.Mobject:
        """Construct a Manim Group or VGroup wrapping all child mobjects."""
        mobjects = [child.manim_object for child in self._group_children]
        all_vmobject = all(isinstance(mob, manim.VMobject) for mob in mobjects)
        if all_vmobject:
            return manim.VGroup(*mobjects)
        return manim.Group(*mobjects)

    def __len__(self) -> int:
        return len(self._group_children)

    def __getitem__(self, index: int) -> Component:
        return self._group_children[index]

    def __iter__(self) -> Iterator[Component]:
        return iter(self._group_children)


__all__ = [
    "Group",
]
