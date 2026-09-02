"""Animora AI/ML visualization module for mathematical surfaces, classic ML, and optimization."""

from __future__ import annotations

from animora.ml.base import MLComponent, MLTrace, MLTraceStep
from animora.ml.classic import (
    DecisionNode,
    DecisionTreeModel,
    DecisionTreeVisualizer,
    HardMarginSVMModel,
    KMeansModel,
    KMeansVisualizer,
    LinearRegressionModel,
    LinearRegressionVisualizer,
    LogisticRegressionModel,
    LogisticRegressionVisualizer,
    PCAModel,
    PCAVisualizer,
    SVMVisualizer,
    decision_tree,
    kmeans,
    linear_regression,
    logistic_regression,
    pca,
    svm,
)
from animora.ml.optimization.gradient_descent import (
    GradientDescentModel,
    GradientDescentVisualizer,
    gradient_descent,
)
from animora.ml.surface_plot import SurfacePlot
from animora.ml.tensor_grid import TensorGrid
from animora.ml.vector_field import VectorField

__all__ = [
    "DecisionNode",
    "DecisionTreeModel",
    "DecisionTreeVisualizer",
    "GradientDescentModel",
    "GradientDescentVisualizer",
    "HardMarginSVMModel",
    "KMeansModel",
    "KMeansVisualizer",
    "LinearRegressionModel",
    "LinearRegressionVisualizer",
    "LogisticRegressionModel",
    "LogisticRegressionVisualizer",
    "MLComponent",
    "MLTrace",
    "MLTraceStep",
    "PCAModel",
    "PCAVisualizer",
    "SVMVisualizer",
    "SurfacePlot",
    "TensorGrid",
    "VectorField",
    "decision_tree",
    "gradient_descent",
    "kmeans",
    "linear_regression",
    "logistic_regression",
    "pca",
    "svm",
]
