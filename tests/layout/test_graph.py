"""Unit tests for GraphLayout solver."""

from __future__ import annotations

import pytest
from animora.layout.base import LayoutItem
from animora.layout.graph import GraphLayout


def test_graph_layout_spring_deterministic() -> None:
    """Verify spring layout gives deterministic coordinates for connected graph."""
    nodes = ["A", "B", "C", "D"]
    items = [LayoutItem(id=n, width=0.5, height=0.5) for n in nodes]
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")]

    layout1 = GraphLayout(edges=edges, algorithm="spring", scale=2.0, seed=42)
    layout2 = GraphLayout(edges=edges, algorithm="spring", scale=2.0, seed=42)

    res1 = layout1.solve(items)
    res2 = layout2.solve(items)

    assert len(res1.positions) == 4
    for n in nodes:
        assert pytest.approx(res1[n][0], abs=1e-5) == res2[n][0]
        assert pytest.approx(res1[n][1], abs=1e-5) == res2[n][1]


def test_graph_layout_circular() -> None:
    """Verify circular algorithm produces positions within scale radius."""
    nodes = ["1", "2", "3", "4", "5"]
    items = [LayoutItem(id=n, width=0.5, height=0.5) for n in nodes]
    layout = GraphLayout(algorithm="circular", scale=3.0)
    res = layout.solve(items)

    assert len(res.positions) == 5
    for n in nodes:
        pos = res[n]
        dist = (pos[0] ** 2 + pos[1] ** 2) ** 0.5
        assert pytest.approx(dist, abs=1e-2) == 3.0


def test_graph_layout_disconnected_components() -> None:
    """Verify layout solver handles disconnected graph without error."""
    nodes = ["A", "B", "C", "D"]
    items = [LayoutItem(id=n, width=0.5, height=0.5) for n in nodes]
    # Two disconnected components: (A-B) and (C-D)
    edges = [("A", "B"), ("C", "D")]

    layout = GraphLayout(edges=edges, algorithm="spring", scale=2.0)
    res = layout.solve(items)
    assert len(res.positions) == 4


def test_graph_layout_empty_and_single() -> None:
    """Verify empty and single node graph."""
    layout = GraphLayout()
    assert len(layout.solve([]).positions) == 0
    assert len(layout.solve([LayoutItem(id="isolated", width=1.0, height=1.0)]).positions) == 1
