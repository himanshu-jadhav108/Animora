"""Breadth-First Search (BFS) and Depth-First Search (DFS) graph traversals."""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any

from animora.algorithms.trace import OperationTrace, OperationType
from animora.core.animation import Animation
from animora.datastructures.graph import Graph, GraphModel
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Breadth-First Search (BFS)
# -----------------------------------------------------------------------------
def bfs_trace(graph_model: GraphModel, start: Any) -> tuple[list[Any], OperationTrace]:
    """Execute BFS traversal on GraphModel, returning (visited_order, operation_trace)."""
    visited_order: list[Any] = []
    trace = OperationTrace()
    visited: set[Any] = {start}
    queue: deque[Any] = deque([start])

    trace.add_step(OperationType.VISIT_NODE, f"Start BFS at node {start}", targets=(start,))
    visited_order.append(start)

    while queue:
        u = queue.popleft()
        for v in graph_model.neighbors(u):
            trace.add_step(OperationType.HIGHLIGHT_EDGE, f"Explore edge ({u}, {v})", targets=(u, v))
            if v not in visited:
                visited.add(v)
                visited_order.append(v)
                queue.append(v)
                trace.add_step(OperationType.VISIT_NODE, f"Visit node {v}", targets=(v,))

    return visited_order, trace


def bfs(graph: Graph, start: Any, run_time: float | None = None) -> list[Animation]:
    """Generate animations for BFS on a Graph component."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.normal

    _, trace = bfs_trace(graph.model, start)
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.VISIT_NODE:
            node = step.targets[0]
            animations.append(graph.animate_mark_visited(node, color=active_theme.colors.success, run_time=duration))
        elif step.op_type == OperationType.HIGHLIGHT_EDGE:
            u, v = step.targets
            animations.append(graph.animate_highlight_edge(u, v, color=active_theme.colors.accent, run_time=duration))

    return animations


# -----------------------------------------------------------------------------
# 2. Depth-First Search (DFS)
# -----------------------------------------------------------------------------
def dfs_trace(graph_model: GraphModel, start: Any) -> tuple[list[Any], OperationTrace]:
    """Execute DFS traversal on GraphModel, returning (visited_order, operation_trace)."""
    visited_order: list[Any] = []
    trace = OperationTrace()
    visited: set[Any] = set()

    def _dfs_rec(u: Any) -> None:
        visited.add(u)
        visited_order.append(u)
        trace.add_step(OperationType.VISIT_NODE, f"Visit node {u}", targets=(u,))

        for v in graph_model.neighbors(u):
            trace.add_step(OperationType.HIGHLIGHT_EDGE, f"Explore edge ({u}, {v})", targets=(u, v))
            if v not in visited:
                _dfs_rec(v)

    _dfs_rec(start)
    return visited_order, trace


def dfs(graph: Graph, start: Any, run_time: float | None = None) -> list[Animation]:
    """Generate animations for DFS on a Graph component."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.normal

    _, trace = dfs_trace(graph.model, start)
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.VISIT_NODE:
            node = step.targets[0]
            animations.append(graph.animate_mark_visited(node, color=active_theme.colors.success, run_time=duration))
        elif step.op_type == OperationType.HIGHLIGHT_EDGE:
            u, v = step.targets
            animations.append(graph.animate_highlight_edge(u, v, color=active_theme.colors.accent, run_time=duration))

    return animations


__all__ = [
    "bfs",
    "bfs_trace",
    "dfs",
    "dfs_trace",
]
