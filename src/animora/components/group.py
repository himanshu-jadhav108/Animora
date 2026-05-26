"""Group composite component for bundling multiple components into a single unit."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator
import manim

from animora.core.component import Component
from animora.core.config import ComponentConfig

if TYPE_CHECKING:
    from typing_extensions import Self


class Group(Component):
    """A composite container component for grouping multiple components.

    Allows treating a collection of components as a single structural unit,
    supporting collective transformations, animations, and indexing.

    Example:
    ```python
    node = Shape.circle(radius=0.5)
    label = Text("A", font_size=24)
    item = Group(node, label)
    item.move_to([2, 2, 0])
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

    def _build_mobject(self) -> manim.Mobject:
        """Construct a Manim Group or VGroup wrapping all child mobjects."""
        mobjects = [child.manim_object for child in self._group_children]
        # If all children are VMobjects, use VGroup; otherwise Group
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
