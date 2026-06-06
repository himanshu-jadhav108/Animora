"""Shortest path and pathfinding algorithms (Dijkstra and A*)."""

from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, Any, Callable

from animora.algorithms.trace import OperationTrace, OperationType
from animora.core.animation import Animation
from animora.datastructures.graph import Graph, GraphModel
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Dijkstra's Algorithm (Uniform Exploration)
# -----------------------------------------------------------------------------
def dijkstra_trace(
    graph_model: GraphModel,
    start: Any,
    target: Any | None = None,
) -> tuple[dict[Any, float], list[Any], OperationTrace]:
    """Execute Dijkstra's algorithm, returning (distances, path, operation_trace)."""
    trace = OperationTrace()
    distances: dict[Any, float] = {node: float("inf") for node in graph_model.nodes()}
    predecessors: dict[Any, Any | None] = {node: None for node in graph_model.nodes()}

    distances[start] = 0.0
    pq: list[tuple[float, Any]] = [(0.0, start)]

    trace.add_step(OperationType.VISIT_NODE, f"Initialize Dijkstra with start {start} (d=0)", targets=(start,))

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist > distances[u]:
            continue

        trace.add_step(OperationType.VISIT_NODE, f"Expand node {u} with current distance {curr_dist}", targets=(u,))

        if target is not None and u == target:
            break

        # Check neighbors
        for v, weight in graph_model.adj.get(u, []):
            w = 1.0 if weight is None else float(weight)
            alt = curr_dist + w
            trace.add_step(OperationType.HIGHLIGHT_EDGE, f"Check edge ({u}, {v}) weight={w}", targets=(u, v))

            if alt < distances[v]:
                distances[v] = alt
                predecessors[v] = u
                heapq.heappush(pq, (alt, v))
                trace.add_step(
                    OperationType.RELAX_EDGE,
                    f"Relax distance to {v}: new distance = {alt}",
                    targets=(u, v),
                    new_distance=alt,
                )

    # Reconstruct path
    path: list[Any] = []
    if target is not None and distances[target] < float("inf"):
        curr: Any | None = target
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()

    return distances, path, trace


def dijkstra(
    graph: Graph,
    start: Any,
    target: Any | None = None,
    run_time: float | None = None,
) -> list[Animation]:
    """Generate animations for Dijkstra's shortest path algorithm."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.normal

    _, path, trace = dijkstra_trace(graph.model, start, target)
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.VISIT_NODE:
            u = step.targets[0]
            animations.append(graph.animate_mark_visited(u, color=active_theme.colors.accent, run_time=duration))
        elif step.op_type == OperationType.RELAX_EDGE:
            u, v = step.targets
            animations.append(graph.animate_highlight_edge(u, v, color=active_theme.colors.success, run_time=duration))

    # Highlight final shortest path
    if len(path) > 1:
        for i in range(len(path) - 1):
            animations.append(graph.animate_highlight_edge(path[i], path[i + 1], color=active_theme.colors.primary, run_time=duration))

    return animations


# -----------------------------------------------------------------------------
# 2. A* Pathfinding (Heuristic-Guided Search)
# -----------------------------------------------------------------------------
def a_star_trace(
    graph_model: GraphModel,
    start: Any,
    goal: Any,
    heuristic: Callable[[Any, Any], float] | None = None,
) -> tuple[list[Any], OperationTrace]:
    """Execute A* heuristic search, returning (path, operation_trace)."""
    h_func = heuristic or (lambda u, v: 0.0)
    trace = OperationTrace()

    g_score: dict[Any, float] = {node: float("inf") for node in graph_model.nodes()}
    f_score: dict[Any, float] = {node: float("inf") for node in graph_model.nodes()}
    came_from: dict[Any, Any | None] = {node: None for node in graph_model.nodes()}

    g_score[start] = 0.0
    f_score[start] = h_func(start, goal)

    pq: list[tuple[float, float, Any]] = [(f_score[start], 0.0, start)]

    trace.add_step(
        OperationType.VISIT_NODE,
        f"Initialize A* at {start} (g=0, h={f_score[start]:.1f}, f={f_score[start]:.1f})",
        targets=(start,),
        f_score=f_score[start],
    )

    while pq:
        curr_f, curr_g, u = heapq.heappop(pq)

        trace.add_step(
            OperationType.VISIT_NODE,
            f"A* selects node {u} with priority f={curr_f:.1f} (g={curr_g:.1f})",
            targets=(u,),
            f_score=curr_f,
        )

        if u == goal:
            break

        for v, weight in graph_model.adj.get(u, []):
            w = 1.0 if weight is None else float(weight)
            tentative_g = curr_g + w

            if tentative_g < g_score[v]:
                came_from[v] = u
                g_score[v] = tentative_g
                h_val = h_func(v, goal)
                f_val = tentative_g + h_val
                f_score[v] = f_val
                heapq.heappush(pq, (f_val, tentative_g, v))

                trace.add_step(
                    OperationType.RELAX_EDGE,
                    f"A* heuristic update to {v}: g={tentative_g:.1f}, h={h_val:.1f}, f={f_val:.1f}",
                    targets=(u, v),
                    g_score=tentative_g,
                    h_score=h_val,
                    f_score=f_val,
                )

    # Reconstruct path
    path: list[Any] = []
    if g_score[goal] < float("inf"):
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()

    return path, trace


def a_star(
    graph: Graph,
    start: Any,
    goal: Any,
    heuristic: Callable[[Any, Any], float] | None = None,
    run_time: float | None = None,
) -> list[Animation]:
    """Generate animations for A* heuristic pathfinding on a Graph component."""
    active_theme = get_active_theme()
    duration = run_time or active_theme.timing.normal

    path, trace = a_star_trace(graph.model, start, goal, heuristic)
    animations: list[Animation] = []

    for step in trace:
        if step.op_type == OperationType.VISIT_NODE:
            u = step.targets[0]
            animations.append(graph.animate_mark_visited(u, color=active_theme.colors.secondary, run_time=duration))
        elif step.op_type == OperationType.RELAX_EDGE:
            u, v = step.targets
            animations.append(graph.animate_highlight_edge(u, v, color=active_theme.colors.warning, run_time=duration))

    if len(path) > 1:
        for i in range(len(path) - 1):
            animations.append(graph.animate_highlight_edge(path[i], path[i + 1], color=active_theme.colors.success, run_time=duration))

    return animations


__all__ = [
    "a_star",
    "a_star_trace",
    "dijkstra",
    "dijkstra_trace",
]
