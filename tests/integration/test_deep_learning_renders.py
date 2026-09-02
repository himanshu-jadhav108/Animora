"""Integration tests verifying full render of deep learning scenes in Manim dry-run mode."""

from __future__ import annotations

import manim

from animora.core.scene import Scene
from animora.ml.deep_learning import (
    NeuralNetworkModel,
    adam,
    backpropagation,
    cnn_convolution,
    momentum,
    neural_network_forward,
    rnn_forward,
    sgd,
)
from animora.theme.builtin import ModernDark
from animora.theme.context import use_theme


class NeuralNetworkForwardScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            self.play(*neural_network_forward([2, 3, 1], [0.5, -0.5]))


class BackpropagationScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            net = NeuralNetworkModel([2, 2, 1], activation="sigmoid")
            self.play(*backpropagation(net, [0.5, 0.5], [1.0]))


class OptimizersScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):

            def loss(x: float, y: float) -> float:
                return x**2 + y**2

            self.play(*sgd(loss, steps=2))
            self.play(*momentum(loss, steps=2))
            self.play(*adam(loss, steps=2))


class CNNConvolutionScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            img = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
            kernel = [[1.0, 0.0], [0.0, 1.0]]
            self.play(*cnn_convolution(img, kernel))


class RNNCellScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            inputs = [[1.0, 0.0], [0.0, 1.0]]
            self.play(*rnn_forward(inputs, hidden_dim=2))


def test_neural_network_forward_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = NeuralNetworkForwardScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_backpropagation_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = BackpropagationScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_optimizers_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = OptimizersScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_cnn_convolution_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = CNNConvolutionScene()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_rnn_cell_renders() -> None:
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = RNNCellScene()
        scene.render()
        assert len(scene.mobjects) >= 1
