"""Tree layout solver for hierarchical structures with arbitrary branching factor."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class TreeLayout(BaseLayout):
    """Hierarchical layout solver positioning tree nodes with non-overlapping subtrees.

    Computes 3D coordinates for trees with arbitrary branching factors,
    allocating subtree widths dynamically to ensure clean visual separation.

    Example:
    ```python
    layout = TreeLayout(
        edges=[("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")],
        root_id="A",
        node_spacing=1.0,
        level_spacing=1.2,
    )
    result = layout.solve(items)
    ```
    """

    def __init__(
        self,
        edges: Sequence[tuple[str, str]] | Mapping[str, Sequence[str]] | None = None,
        root_id: str | None = None,
        node_spacing: float = 1.0,
        level_spacing: float = 1.2,
        direction: str = "down",
        center_origin: bool = True,
    ) -> None:
        self.edges = edges or []
        self.root_id = root_id
        self.node_spacing = float(node_spacing)
        self.level_spacing = float(level_spacing)
        self.direction = direction.lower()
        self.center_origin = center_origin

    def _build_adjacency(
        self,
        items: Sequence[LayoutItem],
    ) -> tuple[str | None, dict[str, list[str]]]:
        """Construct adjacency graph and identify the root node."""
        children_map: dict[str, list[str]] = defaultdict(list)
        all_children: set[str] = set()
        all_nodes: set[str] = {item.id for item in items}

        if isinstance(self.edges, Mapping):
            for parent, kids in self.edges.items():
                for k in kids:
                    children_map[parent].append(k)
                    all_children.add(k)
        else:
            for parent, child in self.edges:
                children_map[parent].append(child)
                all_children.add(child)

        # Determine root
        root: str | None = None
        if self.root_id and self.root_id in all_nodes:
            root = self.root_id
        else:
            roots = list(all_nodes - all_children)
            root = roots[0] if roots else (items[0].id if items else None)

        return root, children_map

    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        if not items:
            return LayoutResult(positions={}, total_width=0.0, total_height=0.0)

        # Allow passing edges or root dynamically
        edges_override = kwargs.get("edges")
        if edges_override is not None:
            self.edges = edges_override
        root_override = kwargs.get("root_id")
        if root_override is not None:
            self.root_id = root_override

        root, children_map = self._build_adjacency(items)
        if root is None:
            return LayoutResult(positions={it.id: (0.0, 0.0, 0.0) for it in items})

        # Dictionary mapping node_id -> item
        item_map = {it.id: it for it in items}

        # 1. Post-order traversal to compute subtree widths and local x positions
        node_x: dict[str, float] = {}
        node_y: dict[str, float] = {}
        subtree_width: dict[str, float] = {}

        next_leaf_x: float = 0.0

        def layout_subtree(u: str, depth: int) -> None:
            nonlocal next_leaf_x
            children = children_map.get(u, [])
            item_w = item_map[u].width if u in item_map else 1.0

            node_y[u] = -depth * self.level_spacing

            if not children:
                node_x[u] = next_leaf_x + (item_w / 2.0)
                next_leaf_x += item_w + self.node_spacing
                subtree_width[u] = item_w
            else:
                for v in children:
                    if v in item_map:
                        layout_subtree(v, depth + 1)

                valid_children = [v for v in children if v in node_x]
                if valid_children:
                    leftmost = node_x[valid_children[0]]
                    rightmost = node_x[valid_children[-1]]
                    node_x[u] = (leftmost + rightmost) / 2.0
                    subtree_width[u] = sum(subtree_width.get(v, item_w) for v in valid_children)
                else:
                    node_x[u] = next_leaf_x + (item_w / 2.0)
                    next_leaf_x += item_w + self.node_spacing
                    subtree_width[u] = item_w

        # Run DFS starting at root
        layout_subtree(root, depth=0)

        # Handle any disconnected nodes
        for it in items:
            if it.id not in node_x:
                node_x[it.id] = next_leaf_x + (it.width / 2.0)
                node_y[it.id] = 0.0
                next_leaf_x += it.width + self.node_spacing

        # Center calculation
        all_xs = list(node_x.values())
        all_ys = list(node_y.values())
        min_x, max_x = min(all_xs), max(all_xs)
        min_y, max_y = min(all_ys), max(all_ys)
        total_w = max_x - min_x
        total_h = max_y - min_y

        offset_x = (min_x + max_x) / 2.0 if self.center_origin else 0.0
        offset_y = (min_y + max_y) / 2.0 if self.center_origin else 0.0

        positions: dict[str, tuple[float, float, float]] = {}
        for it in items:
            raw_x = node_x.get(it.id, 0.0) - offset_x
            raw_y = node_y.get(it.id, 0.0) - offset_y

            # Handle direction
            if self.direction == "up":
                final_x, final_y = raw_x, -raw_y
            elif self.direction == "right":
                final_x, final_y = -raw_y, raw_x
            elif self.direction == "left":
                final_x, final_y = raw_y, raw_x
            else:  # "down"
                final_x, final_y = raw_x, raw_y

            positions[it.id] = (final_x, final_y, 0.0)

        return LayoutResult(
            positions=positions,
            total_width=total_w,
            total_height=total_h,
        )


__all__ = [
    "TreeLayout",
]
