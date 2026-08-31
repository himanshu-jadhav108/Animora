"""Binary Search Tree (BST) data structure component with path-traced operations."""

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
class BSTNode:
    """Node in a Binary Search Tree."""

    def __init__(
        self,
        value: float | int,
        left: BSTNode | None = None,
        right: BSTNode | None = None,
    ) -> None:
        self.value: float | int = value
        self.left: BSTNode | None = left
        self.right: BSTNode | None = right


class BSTModel:
    """Pure Python Binary Search Tree model with tracked operation traces."""

    def __init__(self, initial_values: Sequence[float | int] | None = None) -> None:
        self.root: BSTNode | None = None
        for val in initial_values or []:
            self.insert(val)

    def insert(self, value: float | int) -> list[float | int]:
        """Insert value into BST. Returns the sequence of node values traversed."""
        trace: list[float | int] = []
        if self.root is None:
            self.root = BSTNode(value)
            return trace

        curr: BSTNode = self.root
        while True:
            trace.append(curr.value)
            if value < curr.value:
                if curr.left is None:
                    curr.left = BSTNode(value)
                    break
                curr = curr.left
            elif value > curr.value:
                if curr.right is None:
                    curr.right = BSTNode(value)
                    break
                curr = curr.right
            else:
                # Value already exists
                break
        return trace

    def search(self, value: float | int) -> tuple[bool, list[float | int]]:
        """Search for value in BST. Returns (found, traversal_trace)."""
        trace: list[float | int] = []
        curr = self.root

        while curr is not None:
            trace.append(curr.value)
            if value == curr.value:
                return True, trace
            elif value < curr.value:
                curr = curr.left
            else:
                curr = curr.right

        return False, trace

    def delete(self, value: float | int) -> tuple[bool, str, list[float | int]]:
        """Delete value from BST handling all 3 cases: leaf, 1-child, 2-children.

        Returns (success, case_description, trace).
        """
        trace: list[float | int] = []
        deleted = False
        case_name = "not_found"

        def _min_value_node(node: BSTNode) -> BSTNode:
            current = node
            while current.left is not None:
                current = current.left
            return current

        def _delete_helper(root: BSTNode | None, val: float | int) -> BSTNode | None:
            nonlocal deleted, case_name
            if root is None:
                return None

            trace.append(root.value)
            if val < root.value:
                root.left = _delete_helper(root.left, val)
            elif val > root.value:
                root.right = _delete_helper(root.right, val)
            else:
                deleted = True
                # Case 1: Leaf
                if root.left is None and root.right is None:
                    case_name = "leaf"
                    return None
                # Case 2: One child (only right or only left)
                elif root.left is None:
                    case_name = "one_child"
                    return root.right
                elif root.right is None:
                    case_name = "one_child"
                    return root.left
                # Case 3: Two children (in-order successor)
                else:
                    case_name = "two_children"
                    successor = _min_value_node(root.right)
                    root.value = successor.value
                    root.right = _delete_helper(root.right, successor.value)

            return root

        self.root = _delete_helper(self.root, value)
        return deleted, case_name, trace

    def in_order_traversal(self) -> list[float | int]:
        """Return in-order sorted list of elements."""
        result: list[float | int] = []

        def _inorder(node: BSTNode | None) -> None:
            if node is not None:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)

        _inorder(self.root)
        return result


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class BST(Component):
    """Visual Binary Search Tree component.

    Positions nodes using TreeLayout and animates path traversal before
    insertions, searches, and deletions.

    Example:
    ```python
    bst = BST([50, 30, 70, 20, 40])
    scene.play(bst.animate_insert(35))
    scene.play(bst.animate_search(40))
    scene.play(bst.animate_delete(30))
    ```
    """

    def __init__(
        self,
        values: Sequence[float | int] | None = None,
        *,
        node_radius: float = 0.4,
        level_height: float = 1.2,
        sibling_spacing: float = 1.2,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = BSTModel(values)
        self._node_radius = float(node_radius)
        self._level_height = float(level_height)
        self._sibling_spacing = float(sibling_spacing)

        self._node_map: dict[float | int, Group] = {}
        self._edges: list[Connector] = []
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> BSTModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Construct BST visual nodes and connectors positioned via TreeLayout."""
        active_theme = get_active_theme()

        self._node_map = {}
        self._edges = []
        all_mobjects: list[manim.Mobject] = []

        if self._model.root is None:
            return manim.VGroup()

        tree_dict: dict[str, list[str]] = {}
        node_components: list[Group] = []

        def _collect(curr: BSTNode) -> None:
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

            children_keys: list[str] = []
            if curr.left is not None:
                children_keys.append(str(curr.left.value))
            if curr.right is not None:
                children_keys.append(str(curr.right.value))

            tree_dict[node_key] = children_keys

            if curr.left is not None:
                _collect(curr.left)
            if curr.right is not None:
                _collect(curr.right)

        _collect(self._model.root)

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

        def _connect(curr: BSTNode) -> None:
            parent_grp = self._node_map[curr.value]
            for child in [curr.left, curr.right]:
                if child is not None:
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

    def animate_insert(self, value: float | int, run_time: float | None = None) -> Animation:
        """Insert value, tracing the comparison path before adding new node."""
        trace = self._model.insert(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.slow

        # Highlight traversal steps
        highlights: list[manim.Animation] = []
        for val in trace:
            if val in self._node_map:
                grp = self._node_map[val]
                highlights.append(
                    manim.Indicate(grp.manim_object, color=active_theme.colors.accent)
                )

        if not highlights:
            highlights.append(manim.FadeIn(self.manim_object))

        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(*highlights, lag_ratio=0.3, run_time=duration),
            run_time=duration,
            name=f"insert({value}) -> trace={trace}",
        )

    def animate_search(self, value: float | int, run_time: float | None = None) -> Animation:
        """Search value and animate traversal path."""
        found, trace = self._model.search(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.slow

        target_color = active_theme.colors.success if found else active_theme.colors.error
        highlights: list[manim.Animation] = []

        for idx, val in enumerate(trace):
            if val in self._node_map:
                grp = self._node_map[val]
                col = target_color if idx == len(trace) - 1 else active_theme.colors.accent
                highlights.append(manim.Indicate(grp.manim_object, color=col))

        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(*highlights, lag_ratio=0.3, run_time=duration),
            run_time=duration,
            name=f"search({value}) -> found={found}",
        )

    def animate_delete(self, value: float | int, run_time: float | None = None) -> Animation:
        """Delete value and animate deletion trace."""
        _deleted, case_name, _trace = self._model.delete(value)
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        return Animation(
            component=self,
            manim_animation=manim.Indicate(self.manim_object, color=active_theme.colors.error),
            run_time=duration,
            name=f"delete({value}) -> case={case_name}",
        )


__all__ = [
    "BST",
    "BSTModel",
    "BSTNode",
]
