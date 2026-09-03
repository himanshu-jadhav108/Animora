"""Automated verification test executing every example scene in examples/."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import manim


def _load_scene_from_file(rel_path: str, scene_class_name: str) -> Any:
    """Dynamically load a scene class from an example file path."""
    file_path = Path(__file__).parent.parent.parent / "examples" / rel_path
    mod_name = f"example_module_{rel_path.replace('.', '_')}"
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, scene_class_name)


def test_example_01_basics_and_shapes() -> None:
    scene_cls = _load_scene_from_file("01_basics_and_shapes.py", "BasicsAndShapesScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_02_layout_and_grouping() -> None:
    scene_cls = _load_scene_from_file("02_layout_and_grouping.py", "LayoutAndGroupingScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_03_themes_and_styling() -> None:
    scene_cls = _load_scene_from_file("03_themes_and_styling.py", "ThemesAndStylingScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_04_dataviz_charts() -> None:
    scene_cls = _load_scene_from_file("04_dataviz_charts.py", "DataVizChartsScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_05_datastructures_bst() -> None:
    scene_cls = _load_scene_from_file("05_datastructures_bst.py", "BSTDataStructureScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_06_algorithms_sorting() -> None:
    scene_cls = _load_scene_from_file("06_algorithms_sorting.py", "QuickSortAlgorithmScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_07_pathfinding_dijkstra() -> None:
    scene_cls = _load_scene_from_file("07_pathfinding_dijkstra.py", "DijkstraPathfindingScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_08_ai_ml_foundations() -> None:
    scene_cls = _load_scene_from_file("08_ai_ml_foundations.py", "AIMLFoundationsScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_09_classic_machine_learning() -> None:
    scene_cls = _load_scene_from_file("09_classic_machine_learning.py", "ClassicMLScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_10_deep_learning_and_backprop() -> None:
    scene_cls = _load_scene_from_file("10_deep_learning_and_backprop.py", "DeepLearningScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_example_11_nlp_and_attention() -> None:
    scene_cls = _load_scene_from_file("11_nlp_and_attention.py", "NLPAndAttentionScene")
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = scene_cls()
        scene.render()
        assert len(scene.mobjects) >= 1
