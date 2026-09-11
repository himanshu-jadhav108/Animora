"""Reusable presentation templates for rapid scene development in Animora.

Provides production-ready, styled base scene scaffolds for algorithm walkthroughs,
data comparisons, data structure operations, and machine learning architectures.
"""

from __future__ import annotations

from animora.templates.algorithm_explainer import AlgorithmExplainerTemplate
from animora.templates.base import BaseTemplateScene
from animora.templates.data_comparison import DataComparisonTemplate
from animora.templates.data_structure_walkthrough import DataStructureWalkthroughTemplate
from animora.templates.neural_network_explainer import NeuralNetworkExplainerTemplate

TEMPLATES: dict[str, type[BaseTemplateScene]] = {
    "algorithm_explainer": AlgorithmExplainerTemplate,
    "data_comparison": DataComparisonTemplate,
    "data_structure_walkthrough": DataStructureWalkthroughTemplate,
    "neural_network_explainer": NeuralNetworkExplainerTemplate,
}


def list_templates() -> list[str]:
    """Return a list of available template identifiers."""
    return sorted(TEMPLATES.keys())


def get_template(name: str) -> type[BaseTemplateScene]:
    """Retrieve a template class by identifier."""
    key = name.strip().lower().replace("-", "_")
    if key in TEMPLATES:
        return TEMPLATES[key]
    raise KeyError(f"Unknown template '{name}'. Available templates: {list_templates()}")


__all__ = [
    "TEMPLATES",
    "AlgorithmExplainerTemplate",
    "BaseTemplateScene",
    "DataComparisonTemplate",
    "DataStructureWalkthroughTemplate",
    "NeuralNetworkExplainerTemplate",
    "get_template",
    "list_templates",
]
