"""Large-scale stress test scenarios for performance benchmarking."""

from __future__ import annotations

from animora.algorithms.sorting import quick_sort_trace
from animora.components import Group, Shape
from animora.core.scene import Scene
from animora.datastructures.array import Array
from animora.datastructures.bst import BST
from animora.datastructures.graph import Graph
from animora.layout.circular import CircularLayout
from animora.layout.grid import GridLayout
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class LargeArrayStressScene(Scene):
    """Stress scenario: 100-element Array component with quick sort operation trace."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            values = list(range(100, 0, -1))
            arr = Array(values, cell_width=0.4, cell_height=0.4)
            # Generate trace
            _, trace = quick_sort_trace(arr.model.to_list())
            assert len(trace) > 100


class LargeTreeStressScene(Scene):
    """Stress scenario: 100-node Binary Search Tree with layout solving."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # Deterministic pseudo-random sequence
            values = [(i * 37) % 500 for i in range(100)]
            bst = BST(values, node_radius=0.15, level_height=0.6, sibling_spacing=0.6)
            assert len(bst.model.in_order_traversal()) == len(set(values))


class LargeGridStressScene(Scene):
    """Stress scenario: 256-element Group positioned via GridLayout."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            nodes = [Shape.circle(radius=0.1) for _ in range(256)]
            grp = Group(*nodes)
            grp.arrange(GridLayout(columns=16, col_spacing=0.1, row_spacing=0.1))
            assert len(grp.children) == 256
