"""Unit tests verifying GraphModel adjacency and edge representation."""

from __future__ import annotations

from animora.datastructures.graph import GraphModel


def test_graph_model_undirected_operations() -> None:
    """Verify undirected graph adjacency and edge lookups."""
    g = GraphModel(directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")

    assert set(g.nodes()) == {"A", "B", "C"}
    assert set(g.neighbors("B")) == {"A", "C"}
    assert len(g.edges()) == 3

    # Remove edge
    removed = g.remove_edge("A", "B")
    assert removed is True
    assert "B" not in g.neighbors("A")
    assert "A" not in g.neighbors("B")


def test_graph_model_directed_operations() -> None:
    """Verify directed graph asymmetric adjacency."""
    g = GraphModel(directed=True)
    g.add_edge("A", "B")

    assert "B" in g.neighbors("A")
    assert "A" not in g.neighbors("B")
