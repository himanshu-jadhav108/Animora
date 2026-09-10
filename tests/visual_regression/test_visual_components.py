"""Visual regression tests covering core Animora visual components.

Renders deterministic frames using Cairo renderer and verifies against committed baselines:
- Array (construction + swap animation)
- Table (construction + cell highlight)
- BST (construction + node insertion)
- TensorGrid (construction + cell highlight)
- BarChart (construction + bar highlight)
- LineChart (construction + progressive draw)
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from animora.core.scene import Scene
from animora.datastructures.array import Array
from animora.datastructures.bst import BST
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.line_chart import LineChart
from animora.dataviz.table import Table
from animora.ml.tensor_grid import TensorGrid
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class ArrayVisualScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            arr = Array([15, 3, 42, 8])
            self.play(arr.animate_swap(0, 2, run_time=0.2))
            self.wait(0.1)


class TableVisualScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            tbl = Table(
                data=[["10", "20"], ["30", "40"]],
                headers=["X", "Y"],
                row_labels=["R1", "R2"],
            )
            self.play(tbl.animate_highlight_cell(0, 1, run_time=0.2))
            self.wait(0.1)


class BSTVisualScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            bst = BST([50, 25, 75])
            self.play(bst.animate_insert(40, run_time=0.2))
            self.wait(0.1)


class TensorGridVisualScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            tg = TensorGrid(
                shape=(2, 3),
                values=[[1, 2, 3], [4, 5, 6]],
            )
            self.play(tg.animate_highlight_cell(0, 2, run_time=0.2))
            self.wait(0.1)


class BarChartVisualScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            bc = BarChart(
                data=[25.0, 50.0, 75.0],
                bar_labels=["Alpha", "Beta", "Gamma"],
            )
            self.play(bc.animate_highlight_bar(1, run_time=0.2))
            self.wait(0.1)


class LineChartVisualScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            lc = LineChart(
                points=[(0.0, 10.0), (1.0, 25.0), (2.0, 15.0)],
            )
            self.play(lc.animate_draw(run_time=0.2))
            self.wait(0.1)


@pytest.mark.visual_regression
def test_visual_array(assert_visual_match: Callable[..., None]) -> None:
    assert_visual_match(ArrayVisualScene, "array_swap")


@pytest.mark.visual_regression
def test_visual_table(assert_visual_match: Callable[..., None]) -> None:
    assert_visual_match(TableVisualScene, "table_highlight_cell")


@pytest.mark.visual_regression
def test_visual_bst(assert_visual_match: Callable[..., None]) -> None:
    assert_visual_match(BSTVisualScene, "bst_insert")


@pytest.mark.visual_regression
def test_visual_tensor_grid(assert_visual_match: Callable[..., None]) -> None:
    assert_visual_match(TensorGridVisualScene, "tensor_grid_highlight")


@pytest.mark.visual_regression
def test_visual_bar_chart(assert_visual_match: Callable[..., None]) -> None:
    assert_visual_match(BarChartVisualScene, "bar_chart_highlight")


@pytest.mark.visual_regression
def test_visual_line_chart(assert_visual_match: Callable[..., None]) -> None:
    assert_visual_match(LineChartVisualScene, "line_chart_draw")
