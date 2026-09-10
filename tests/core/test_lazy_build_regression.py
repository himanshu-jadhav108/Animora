"""Regression tests for BUG-001: Lazy-build IndexError and uninitialized state.

Verifies that calling animation/mutation methods directly on freshly instantiated
components (before explicit .render() or scene.add()) correctly initializes the
underlying Manim representations and produces valid Animation objects without raising
IndexError or AttributeError.
"""

from __future__ import annotations

from animora.core.animation import Animation
from animora.datastructures.array import Array
from animora.datastructures.bst import BST
from animora.datastructures.graph import Graph
from animora.datastructures.hash_table import HashTable
from animora.datastructures.linked_list import LinkedList
from animora.datastructures.queue import Queue
from animora.datastructures.stack import Stack
from animora.datastructures.tree import Tree
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.histogram import Histogram
from animora.dataviz.line_chart import LineChart
from animora.dataviz.scatter_plot import ScatterPlot
from animora.dataviz.table import Table
from animora.ml.tensor_grid import TensorGrid


def test_array_lazy_build_animations() -> None:
    arr = Array([10, 20, 30, 40])
    swap_anim = arr.animate_swap(0, 3)
    assert isinstance(swap_anim, Animation)
    assert swap_anim.to_manim() is not None

    highlight_anim = arr.animate_highlight(1)
    assert isinstance(highlight_anim, Animation)

    set_anim = arr.animate_set(2, 99)
    assert isinstance(set_anim, Animation)


def test_table_lazy_build_animations() -> None:
    tbl = Table(
        data=[["1", "2"], ["3", "4"]],
        headers=["A", "B"],
        row_labels=["R1", "R2"],
    )
    anim = tbl.animate_highlight_cell(0, 1)
    assert isinstance(anim, Animation)
    assert anim.to_manim() is not None
    assert tbl.get_cell(0, 0) is not None


def test_bar_chart_lazy_build_animations() -> None:
    bc = BarChart(data=[10.0, 20.0, 30.0], bar_labels=["A", "B", "C"])
    grow_anim = bc.animate_grow()
    assert isinstance(grow_anim, Animation)

    hl_anim = bc.animate_highlight_bar(1)
    assert isinstance(hl_anim, Animation)


def test_histogram_lazy_build_animations() -> None:
    hist = Histogram(data=[1.0, 1.5, 2.0, 2.5, 3.0], bins=3)
    grow_anim = hist.animate_grow()
    assert isinstance(grow_anim, Animation)


def test_line_chart_lazy_build_animations() -> None:
    lc = LineChart(points=[(0.0, 2.0), (1.0, 4.0), (2.0, 6.0)])
    draw_anim = lc.animate_draw()
    assert isinstance(draw_anim, Animation)


def test_scatter_plot_lazy_build_animations() -> None:
    sp = ScatterPlot(points=[(1.0, 3.0), (2.0, 4.0)])
    plot_anim = sp.animate_plot()
    assert isinstance(plot_anim, Animation)


def test_tensor_grid_lazy_build_animations() -> None:
    tg = TensorGrid(shape=(2, 3), values=[[1, 2, 3], [4, 5, 6]])
    hl_anim = tg.animate_highlight_cell(0, 2)
    assert isinstance(hl_anim, Animation)


def test_stack_lazy_build_animations() -> None:
    s = Stack(items=[1, 2, 3])
    push_anim = s.animate_push(4)
    assert isinstance(push_anim, Animation)
    pop_anim = s.animate_pop()
    assert isinstance(pop_anim, Animation)


def test_queue_lazy_build_animations() -> None:
    q = Queue(items=[1, 2, 3])
    enq_anim = q.animate_enqueue(4)
    assert isinstance(enq_anim, Animation)
    deq_anim = q.animate_dequeue()
    assert isinstance(deq_anim, Animation)
    peek_anim = q.animate_peek()
    assert isinstance(peek_anim, Animation)


def test_linked_list_lazy_build_animations() -> None:
    ll = LinkedList([1, 2, 3])
    tail_anim = ll.animate_insert_tail(4)
    assert isinstance(tail_anim, Animation)


def test_hash_table_lazy_build_animations() -> None:
    ht = HashTable(capacity=5)
    ins_anim = ht.animate_insert(2, "val")
    assert isinstance(ins_anim, Animation)
    srch_anim = ht.animate_search(2)
    assert isinstance(srch_anim, Animation)


def test_tree_lazy_build_animations() -> None:
    t = Tree(root_value="A")
    t.model.insert_child("A", "B")
    hl_anim = t.animate_highlight_node("B")
    assert isinstance(hl_anim, Animation)


def test_graph_lazy_build_animations() -> None:
    g = Graph(nodes=["A", "B"], edges=[("A", "B")])
    hl_node = g.animate_highlight_node("A")
    assert isinstance(hl_node, Animation)
    vis_node = g.animate_mark_visited("B")
    assert isinstance(vis_node, Animation)
    hl_edge = g.animate_highlight_edge("A", "B")
    assert isinstance(hl_edge, Animation)


def test_visual_bst_lazy_build_animations() -> None:
    bst = BST([5, 3, 7])
    ins_anim = bst.animate_insert(4)
    assert isinstance(ins_anim, Animation)
    srch_anim = bst.animate_search(3)
    assert isinstance(srch_anim, Animation)
    del_anim = bst.animate_delete(7)
    assert isinstance(del_anim, Animation)
