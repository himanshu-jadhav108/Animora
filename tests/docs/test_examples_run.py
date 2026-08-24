"""Automated verification test executing every example scene in examples/."""

from __future__ import annotations

import manim

from examples.01_basics_and_shapes import BasicsAndShapesScene
from examples.02_layout_and_grouping import LayoutAndGroupingScene
from examples.03_themes_and_styling import ThemesAndStylingScene
from examples.04_dataviz_charts import DataVizChartsScene
from examples.05_datastructures_bst import BSTDataStructureScene
from examples.06_algorithms_sorting import QuickSortAlgorithmScene
from examples.07_pathfinding_dijkstra import DijkstraPathfindingScene


def test_example_01_basics_and_shapes() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = BasicsAndShapesScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_02_layout_and_grouping() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = LayoutAndGroupingScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_03_themes_and_styling() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = ThemesAndStylingScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_04_dataviz_charts() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = DataVizChartsScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_05_datastructures_bst() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = BSTDataStructureScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_06_algorithms_sorting() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = QuickSortAlgorithmScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_07_pathfinding_dijkstra() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = DijkstraPathfindingScene()
        scene.render()
        assert len(scene.mobjects) >= 1
