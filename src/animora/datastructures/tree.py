"""Generic Tree data structure component positioned via Phase 4 TreeLayout."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim

from animora.components.connector import Connector
from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.tree import TreeLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class TreeNode:
    """Node in an N-ary generic tree."""

    def __init__(self, value: Any, children: Sequence[TreeNode] | None = None) -> None:
        self.value: Any = value
        self.children: list[TreeNode] = list(children or [])

    def add_child(self, child_node: TreeNode) -> None:
        self.children.append(child_node)


class GenericTreeModel:
    """Pure Python generic N-ary tree model."""

    def __init__(self, root_value: Any | None = None) -> None:
        self.root: TreeNode | None = TreeNode(root_value) if root_value is not None else None

    def insert_child(self, parent_value: Any, child_value: Any) -> bool:
        """Insert child under first matching parent node. Return True if inserted."""
        if self.root is None:
            self.root = TreeNode(parent_value, [TreeNode(child_value)])
            return True

        parent = self._find_node(self.root, parent_value)
        if parent is not None:
            parent.add_child(TreeNode(child_value))
            return True
        return False

    def _find_node(self, current: TreeNode | None, value: Any) -> TreeNode | None:
        if current is None:
            return None
        if current.value == value:
            return current
        for child in current.children:
            found = self._find_node(child, value)
            if found is not None:
                return found
        return None

    def traverse_preorder(self) -> list[Any]:
        """Return list of node values in preorder sequence."""
        result: list[Any] = []

        def _dfs(node: TreeNode | None) -> None:
            if node is None:
                return
            result.append(node.value)
            for child in node.children:
                _dfs(child)

        _dfs(self.root)
        return result


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class Tree(Component):
    """Visual N-ary Tree component positioned via TreeLayout.

    Example:
    ```python
    tree = Tree(root_value="A")
    tree.model.insert_child("A", "B")
    tree.model.insert_child("A", "C")
    scene.play(tree.animate_create())
    ```
    """

    def __init__(
        self,
        root_value: Any | None = None,
        *,
        node_radius: float = 0.4,
        level_height: float = 1.2,
        sibling_spacing: float = 1.2,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = GenericTreeModel(root_value)
        self._node_radius = float(node_radius)
        self._level_height = float(level_height)
        self._sibling_spacing = float(sibling_spacing)

        self._node_map: dict[Any, Group] = {}
        self._edges: list[Connector] = []
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> GenericTreeModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Construct visual nodes and edges using TreeLayout coordinates."""
        active_theme = get_active_theme()

        self._node_map = {}
        self._edges = []
        all_mobjects: list[manim.Mobject] = []

        if self._model.root is None:
            return manim.VGroup()

        # 1. Flatten nodes and build layout tree representation
        tree_dict: dict[str, list[str]] = {}
        node_components: list[Group] = []

        def _collect(curr: TreeNode) -> None:
            node_key = str(curr.value)
            circle = Shape.circle(
                radius=self._node_radius,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.primary,
                stroke_width=active_theme.strokes.regular,
            )
            txt = Text(
                str(curr.value),
                font_size=active_theme.typography.font_size_sm,
                color=active_theme.colors.text,
            )
            grp = Group(circle, txt)
            self._node_map[curr.value] = grp
            node_components.append(grp)

            tree_dict[node_key] = [str(ch.value) for ch in curr.children]
            for child in curr.children:
                _collect(child)

        _collect(self._model.root)

        # 2. Use Phase 4 TreeLayout to arrange positions
        root_key = str(self._model.root.value)
        layout = TreeLayout(
            edges=tree_dict,
            root_id=root_key,
            level_spacing=self._level_height,
            node_spacing=self._sibling_spacing,
        )

        container = Group(*node_components)
        container.arrange(layout)

        for grp in node_components:
            all_mobjects.append(grp.manim_object)

        # 3. Create connecting connectors between parents and children
        def _connect(curr: TreeNode) -> None:
            parent_grp = self._node_map[curr.value]
            for child in curr.children:
                child_grp = self._node_map[child.value]
                edge = Connector(
                    start=parent_grp,
                    end=child_grp,
                    stroke_color=active_theme.colors.border,
                    stroke_width=active_theme.strokes.regular,
                )
                self._edges.append(edge)
                all_mobjects.append(edge.manim_object)
                _connect(child)

        _connect(self._model.root)
        return manim.VGroup(*all_mobjects)

    def animate_highlight_node(
        self,
        value: Any,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Highlight a specific tree node."""
        active_theme = get_active_theme()
        highlight_col = color or active_theme.colors.accent
        duration = run_time or active_theme.timing.normal

        target_grp = self._node_map[value]
        return Animation(
            component=target_grp,
            manim_animation=manim.Indicate(target_grp.manim_object, color=highlight_col),
            run_time=duration,
            name=f"highlight_node({value})",
        )


__all__ = [
    "GenericTreeModel",
    "Tree",
    "TreeNode",
]
