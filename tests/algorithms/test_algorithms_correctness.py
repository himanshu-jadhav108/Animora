"""Unit tests verifying pure mathematical & computational correctness of all 11 algorithms."""

from __future__ import annotations

import random
from animora.algorithms.backtracking import n_queens_trace
from animora.algorithms.dynamic_programming import fibonacci_dp_trace
from animora.algorithms.graph_traversal import bfs_trace, dfs_trace
from animora.algorithms.pathfinding import a_star_trace, dijkstra_trace
from animora.algorithms.search import binary_search_trace
from animora.algorithms.sorting import (
    bubble_sort_trace,
    insertion_sort_trace,
    merge_sort_trace,
    quick_sort_trace,
    selection_sort_trace,
)
from animora.datastructures.graph import GraphModel


def test_binary_search_correctness() -> None:
    """Verify binary search returns correct index for present and absent keys."""
    sorted_arr = [10, 20, 30, 40, 50, 60, 70, 80]
    for idx, val in enumerate(sorted_arr):
        res_idx, _ = binary_search_trace(sorted_arr, val)
        assert res_idx == idx

    res_idx, _ = binary_search_trace(sorted_arr, 999)
    assert res_idx == -1


def test_sorting_algorithms_correctness() -> None:
    """Verify all 5 sorting algorithms sort random arrays to match Python sorted()."""
    random.seed(42)
    sample = [random.randint(1, 100) for _ in range(20)]
    expected = sorted(sample)

    assert bubble_sort_trace(sample)[0] == expected
    assert selection_sort_trace(sample)[0] == expected
    assert insertion_sort_trace(sample)[0] == expected
    assert merge_sort_trace(sample)[0] == expected
    assert quick_sort_trace(sample)[0] == expected


def test_graph_traversals_correctness() -> None:
    """Verify BFS and DFS visit all reachable nodes."""
    g = GraphModel(directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("A", "D")

    bfs_order, _ = bfs_trace(g, "A")
    assert set(bfs_order) == {"A", "B", "C", "D"}
    assert bfs_order[0] == "A"

    dfs_order, _ = dfs_trace(g, "A")
    assert set(dfs_order) == {"A", "B", "C", "D"}
    assert dfs_order[0] == "A"


def test_dijkstra_shortest_path_correctness() -> None:
    """Verify Dijkstra finds exact shortest path distances."""
    g = GraphModel(directed=True)
    g.add_edge("A", "B", weight=1.0)
    g.add_edge("B", "C", weight=2.0)
    g.add_edge("A", "C", weight=5.0)

    distances, path, _ = dijkstra_trace(g, "A", target="C")
    assert distances["C"] == 3.0
    assert path == ["A", "B", "C"]


def test_a_star_path_correctness() -> None:
    """Verify A* finds shortest path to goal."""
    g = GraphModel(directed=True)
    g.add_edge("Start", "Mid", weight=2.0)
    g.add_edge("Mid", "Goal", weight=3.0)
    g.add_edge("Start", "Goal", weight=10.0)

    path, _ = a_star_trace(g, "Start", "Goal", heuristic=lambda u, v: 0.0)
    assert path == ["Start", "Mid", "Goal"]


def test_fibonacci_dp_correctness() -> None:
    """Verify DP Fibonacci computes correct N-th values."""
    assert fibonacci_dp_trace(0)[0] == 0
    assert fibonacci_dp_trace(1)[0] == 1
    assert fibonacci_dp_trace(6)[0] == 8
    assert fibonacci_dp_trace(10)[0] == 55


def test_n_queens_backtracking_correctness() -> None:
    """Verify N-Queens finds all 2 valid solutions for 4-Queens."""
    solutions, _ = n_queens_trace(4)
    assert len(solutions) == 2
    assert [1, 3, 0, 2] in solutions
    assert [2, 0, 3, 1] in solutions
