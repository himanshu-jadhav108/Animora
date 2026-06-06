"""Algorithm visualizations and operation tracing for Animora.

Provides educational animations and discrete operation traces for searching,
sorting, graph traversals, pathfinding, dynamic programming, and backtracking.
"""

from __future__ import annotations

from animora.algorithms.backtracking import n_queens, n_queens_trace
from animora.algorithms.dynamic_programming import fibonacci_dp, fibonacci_dp_trace
from animora.algorithms.graph_traversal import bfs, bfs_trace, dfs, dfs_trace
from animora.algorithms.pathfinding import (
    a_star,
    a_star_trace,
    dijkstra,
    dijkstra_trace,
)
from animora.algorithms.search import binary_search, binary_search_trace
from animora.algorithms.sorting import (
    bubble_sort,
    bubble_sort_trace,
    insertion_sort,
    insertion_sort_trace,
    merge_sort,
    merge_sort_trace,
    quick_sort,
    quick_sort_trace,
    selection_sort,
    selection_sort_trace,
)
from animora.algorithms.trace import (
    OperationStep,
    OperationTrace,
    OperationType,
)

__all__: list[str] = [
    "OperationStep",
    "OperationTrace",
    "OperationType",
    "a_star",
    "a_star_trace",
    "bfs",
    "bfs_trace",
    "binary_search",
    "binary_search_trace",
    "bubble_sort",
    "bubble_sort_trace",
    "dfs",
    "dfs_trace",
    "dijkstra",
    "dijkstra_trace",
    "fibonacci_dp",
    "fibonacci_dp_trace",
    "insertion_sort",
    "insertion_sort_trace",
    "merge_sort",
    "merge_sort_trace",
    "n_queens",
    "n_queens_trace",
    "quick_sort",
    "quick_sort_trace",
    "selection_sort",
    "selection_sort_trace",
]
