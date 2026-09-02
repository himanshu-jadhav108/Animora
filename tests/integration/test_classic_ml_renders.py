"""Integration tests verifying full render of all 6 classic ML scenes in Manim dry-run mode."""

from __future__ import annotations

import manim

from animora.core.scene import Scene
from animora.ml.classic import (
    decision_tree,
    kmeans,
    linear_regression,
    logistic_regression,
    pca,
    svm,
)
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class LinearRegressionScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            x = [1.0, 2.0, 3.0, 4.0]
            y = [2.0, 4.1, 5.9, 8.2]
            self.play(*linear_regression(x, y, steps=3))


class LogisticRegressionScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            X = [[-1.0, -1.0], [-2.0, -1.0], [1.0, 1.0], [2.0, 1.0]]
            y = [0, 0, 1, 1]
            self.play(*logistic_regression(X, y, steps=3))


class KMeansScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            data = [[-2.0, -2.0], [-1.8, -2.2], [2.0, 2.0], [2.2, 1.9]]
            self.play(*kmeans(data, k=2, max_iters=2))


class DecisionTreeScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            X = [[1.0, 2.0], [1.5, 1.8], [5.0, 5.0], [5.5, 5.2]]
            y = [0, 0, 1, 1]
            self.play(*decision_tree(X, y, max_depth=1))


class SVMScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            X = [[-2.0, 0.0], [-1.0, 0.5], [1.0, -0.5], [2.0, 0.0]]
            y = [-1, -1, 1, 1]
            self.play(*svm(X, y))


class PCAScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            X = [[1.0, 1.0], [2.0, 2.1], [3.0, 2.9], [4.0, 4.2]]
            self.play(*pca(X, n_components=1))


def test_linear_regression_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = LinearRegressionScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_logistic_regression_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = LogisticRegressionScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_kmeans_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = KMeansScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_decision_tree_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = DecisionTreeScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_svm_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = SVMScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_pca_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = PCAScene()
        scene.render()
        assert len(scene.mobjects) >= 1
