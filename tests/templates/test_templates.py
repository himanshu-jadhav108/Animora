"""Unit and integration tests for Animora presentation templates."""

from __future__ import annotations

import manim
import pytest

from animora.templates import (
    AlgorithmExplainerTemplate,
    DataComparisonTemplate,
    DataStructureWalkthroughTemplate,
    NeuralNetworkExplainerTemplate,
    get_template,
    list_templates,
)


def test_template_registry() -> None:
    """Verify registry listing and lookup by identifier."""
    templates = list_templates()
    assert "algorithm_explainer" in templates
    assert "data_comparison" in templates
    assert "data_structure_walkthrough" in templates
    assert "neural_network_explainer" in templates

    assert get_template("algorithm_explainer") is AlgorithmExplainerTemplate
    assert get_template("Data-Comparison") is DataComparisonTemplate

    with pytest.raises(KeyError, match="Unknown template 'non_existent'"):
        get_template("non_existent")


def test_algorithm_explainer_template_renders() -> None:
    """Verify AlgorithmExplainerTemplate executes in dry-run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        scene = AlgorithmExplainerTemplate()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_data_comparison_template_renders() -> None:
    """Verify DataComparisonTemplate executes in dry-run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        scene = DataComparisonTemplate()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_data_structure_walkthrough_template_renders() -> None:
    """Verify DataStructureWalkthroughTemplate executes in dry-run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        scene = DataStructureWalkthroughTemplate()
        scene.render()
        assert len(scene.mobjects) >= 1


def test_neural_network_explainer_template_renders() -> None:
    """Verify NeuralNetworkExplainerTemplate executes in dry-run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        scene = NeuralNetworkExplainerTemplate()
        scene.render()
        assert len(scene.mobjects) >= 1
