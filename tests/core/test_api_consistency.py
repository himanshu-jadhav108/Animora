"""Unit tests verifying API consistency and deprecated aliases across components."""

from __future__ import annotations

import pytest

from animora.core.animation import Animation
from animora.datastructures.graph import Graph
from animora.datastructures.linked_list import LinkedList
from animora.datastructures.tree import Tree
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.table import Table
from animora.ml.tensor_grid import TensorGrid


def test_barchart_animate_highlight_and_deprecation() -> None:
    """Verify BarChart.animate_highlight works and animate_highlight_bar warns."""
    bc = BarChart(data=[10.0, 20.0, 30.0], bar_labels=["A", "B", "C"])
    anim = bc.animate_highlight(1)
    assert isinstance(anim, Animation)

    with pytest.deprecated_call():
        legacy_anim = bc.animate_highlight_bar(1)
        assert isinstance(legacy_anim, Animation)


def test_table_animate_highlight_and_deprecation() -> None:
    """Verify Table.animate_highlight works and animate_highlight_cell warns."""
    tbl = Table(data=[["1", "2"], ["3", "4"]], headers=["A", "B"])
    anim = tbl.animate_highlight(0, 1)
    assert isinstance(anim, Animation)

    with pytest.deprecated_call():
        legacy_anim = tbl.animate_highlight_cell(0, 1)
        assert isinstance(legacy_anim, Animation)


def test_tensor_grid_animate_highlight_and_deprecation() -> None:
    """Verify TensorGrid.animate_highlight works and animate_highlight_cell warns."""
    tg = TensorGrid(shape=(2, 2), values=[[1, 2], [3, 4]])
    anim = tg.animate_highlight(0, 1)
    assert isinstance(anim, Animation)

    with pytest.deprecated_call():
        legacy_anim = tg.animate_highlight_cell(0, 1)
        assert isinstance(legacy_anim, Animation)


def test_tree_animate_highlight_and_deprecation() -> None:
    """Verify Tree.animate_highlight works and animate_highlight_node warns."""
    tree = Tree("root")
    tree.model.insert_child("root", "child")
    anim = tree.animate_highlight("child")
    assert isinstance(anim, Animation)

    with pytest.deprecated_call():
        legacy_anim = tree.animate_highlight_node("child")
        assert isinstance(legacy_anim, Animation)


def test_graph_animate_highlight_and_deprecation() -> None:
    """Verify Graph.animate_highlight works and animate_highlight_node warns."""
    g = Graph(nodes=["A", "B"], edges=[("A", "B")])
    anim = g.animate_highlight("A")
    assert isinstance(anim, Animation)

    with pytest.deprecated_call():
        legacy_anim = g.animate_highlight_node("A")
        assert isinstance(legacy_anim, Animation)


def test_linked_list_animate_insert() -> None:
    """Verify LinkedList.animate_insert works as convenience alias for animate_insert_tail."""
    ll = LinkedList([1, 2, 3])
    anim = ll.animate_insert(4)
    assert isinstance(anim, Animation)
