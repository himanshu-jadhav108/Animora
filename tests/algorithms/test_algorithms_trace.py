"""Unit tests asserting recorded operation traces match hand-computed sequences."""

from __future__ import annotations

from animora.algorithms.pathfinding import a_star_trace, dijkstra_trace
from animora.algorithms.search import binary_search_trace
from animora.algorithms.sorting import bubble_sort_trace
from animora.algorithms.trace import OperationType
from animora.datastructures.graph import GraphModel


def test_binary_search_trace_sequence() -> None:
    """Verify binary search on [10, 20, 30, 40, 50] searching for 40 compares index 2 then 3."""
    data = [10, 20, 30, 40, 50]
    idx, trace = binary_search_trace(data, 40)
    assert idx == 3

    # Step 1: Compare index 2 (val 30)
    assert trace[0].op_type == OperationType.COMPARE
    assert trace[0].metadata["mid"] == 2

    # Step 2: Compare index 3 (val 40)
    assert trace[1].op_type == OperationType.COMPARE
    assert trace[1].metadata["mid"] == 3

    # Step 3: Highlight index 3 found
    assert trace[2].op_type == OperationType.HIGHLIGHT
    assert trace[2].metadata["found"] is True


def test_bubble_sort_trace_hand_traced() -> None:
    """Verify Bubble Sort on [5, 3, 8, 1] performs exactly 3 swaps."""
    data = [5, 3, 8, 1]
    _, trace = bubble_sort_trace(data)

    swaps = [step for step in trace if step.op_type == OperationType.SWAP]
    assert len(swaps) == 4  # (5,3)->(3,5,8,1), (8,1)->(3,5,1,8), (5,1)->(3,1,5,8), (3,1)->(1,3,5,8)
    assert swaps[0].targets == (0, 1)


def test_dijkstra_vs_a_star_trace_distinction() -> None:
    """Verify Dijkstra and A* produce distinct exploration traces on a heuristic test graph."""
    g = GraphModel(directed=True)
    # Start -> Detour (cost 1, but far from Goal)
    # Detour -> DeadEnd (cost 10)
    # Start -> Mid (cost 2, close to Goal)
    # Mid -> Goal (cost 2)
    g.add_edge("S", "Detour", weight=1.0)
    g.add_edge("Detour", "DeadEnd", weight=10.0)
    g.add_edge("S", "Mid", weight=2.0)
    g.add_edge("Mid", "G", weight=2.0)

    # Heuristic estimates straight-line distance to G
    # Detour is far (h=10), Mid is close (h=1)
    heuristics = {"S": 4.0, "Detour": 10.0, "DeadEnd": 15.0, "Mid": 1.0, "G": 0.0}

    # Dijkstra explores "Detour" first because its edge cost is 1.0 < 2.0
    _, _, d_trace = dijkstra_trace(g, "S", target="G")
    dijkstra_visited = [
        step.targets[0] for step in d_trace if step.op_type == OperationType.VISIT_NODE
    ]

    # A* explores "Mid" before "Detour" because f(Mid) = 2+1 = 3 < f(Detour) = 1+10 = 11!
    _, a_trace = a_star_trace(g, "S", "G", heuristic=lambda u, v: heuristics.get(u, 0.0))
    a_star_visited = [
        step.targets[0] for step in a_trace if step.op_type == OperationType.VISIT_NODE
    ]

    assert dijkstra_visited != a_star_visited
    # Dijkstra visits Detour before Mid
    assert dijkstra_visited.index("Detour") < dijkstra_visited.index("Mid")
    # A* visits Mid before Detour
    assert a_star_visited.index("Mid") < (
        a_star_visited.index("Detour") if "Detour" in a_star_visited else 999
    )
