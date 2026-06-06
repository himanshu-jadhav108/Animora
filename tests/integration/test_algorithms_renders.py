"""Integration test verifying all 11 algorithm animations render in Manim."""

from __future__ import annotations

import manim
from animora.algorithms.backtracking import n_queens
from animora.algorithms.dynamic_programming import fibonacci_dp
from animora.algorithms.graph_traversal import bfs, dfs
from animora.algorithms.pathfinding import a_star, dijkstra
from animora.algorithms.search import binary_search
from animora.algorithms.sorting import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from animora.core.scene import Scene
from animora.datastructures.array import Array
from animora.datastructures.graph import Graph
from animora.dataviz.table import Table


class AlgorithmAnimationCompositeScene(Scene):
    """Scene rendering all 11 algorithm animations."""

    def construct(self) -> None:
        # 1. Search
        arr = Array([10, 20, 30, 40, 50])
        self.play(*binary_search(arr, 40, run_time=0.1))

        # 2. Sorting
        a1 = Array([4, 2, 5, 1])
        self.play(*bubble_sort(a1, run_time=0.1))

        a2 = Array([4, 2, 5, 1])
        self.play(*selection_sort(a2, run_time=0.1))

        a3 = Array([4, 2, 5, 1])
        self.play(*insertion_sort(a3, run_time=0.1))

        a4 = Array([4, 2, 5, 1])
        self.play(*merge_sort(a4, run_time=0.1))

        a5 = Array([4, 2, 5, 1])
        self.play(*quick_sort(a5, run_time=0.1))

        # 3. Graph Traversals & Pathfinding
        g = Graph(nodes=["A", "B", "C"], edges=[("A", "B"), ("B", "C"), ("A", "C")])
        self.play(*bfs(g, "A", run_time=0.1))
        self.play(*dfs(g, "A", run_time=0.1))
        self.play(*dijkstra(g, "A", "C", run_time=0.1))
        self.play(*a_star(g, "A", "C", run_time=0.1))

        # 4. DP
        dp_table = Table(data=[["0", "1", "1", "2", "3"]], headers=["0", "1", "2", "3", "4"])
        self.play(*fibonacci_dp(4, table=dp_table, run_time=0.1))

        # 5. Backtracking
        board = Table(data=[["." for _ in range(4)] for _ in range(4)])
        self.play(*n_queens(4, table=board, run_time=0.1))


def test_algorithm_animations_render_end_to_end() -> None:
    """Verify all 11 algorithm animations render cleanly in Manim dry-run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = AlgorithmAnimationCompositeScene()
        scene.render()
        assert len(scene.mobjects) >= 1
