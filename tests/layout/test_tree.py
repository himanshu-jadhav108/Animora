"""Unit tests for TreeLayout solver."""

from __future__ import annotations

import pytest
from animora.layout.base import LayoutItem
from animora.layout.tree import TreeLayout


def test_tree_layout_3_level_uneven_branching() -> None:
    """Verify 3-level tree with uneven branching factor."""
    # Tree topology:
    #         A
    #      /  |  \
    #     B   C   D
    #    / \       \
    #   E   F       G
    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    items = [LayoutItem(id=n, width=0.8, height=0.8) for n in nodes]
    edges = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F"), ("D", "G")]

    layout = TreeLayout(
        edges=edges,
        root_id="A",
        node_spacing=0.5,
        level_spacing=1.5,
        direction="down",
    )
    res = layout.solve(items)

    assert len(res.positions) == 7

    # 1. Depth verification (level_spacing = 1.5)
    # Root A at depth 0
    # B, C, D at depth 1
    # E, F, G at depth 2
    y_A = res["A"][1]
    y_B = res["B"][1]
    y_E = res["E"][1]

    assert pytest.approx(y_A - y_B, abs=1e-3) == 1.5
    assert pytest.approx(y_B - y_E, abs=1e-3) == 1.5
    assert pytest.approx(res["B"][1], abs=1e-3) == res["C"][1]
    assert pytest.approx(res["C"][1], abs=1e-3) == res["D"][1]
    assert pytest.approx(res["E"][1], abs=1e-3) == res["F"][1]

    # 2. Horizontal centering: Parent B must be centered between children E and F
    x_B = res["B"][0]
    x_E = res["E"][0]
    x_F = res["F"][0]
    assert pytest.approx(x_B, abs=1e-3) == (x_E + x_F) / 2.0


def test_tree_layout_empty_and_single() -> None:
    """Verify empty and single node tree."""
    layout = TreeLayout()
    assert len(layout.solve([]).positions) == 0

    res_single = layout.solve([LayoutItem(id="root", width=1.0, height=1.0)])
    assert len(res_single.positions) == 1
    assert res_single["root"] == (0.0, 0.0, 0.0)
