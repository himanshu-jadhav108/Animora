"""Classic machine learning models, visualizers, and one-call animation APIs."""

from __future__ import annotations

from animora.ml.classic.decision_tree import (
    DecisionNode,
    DecisionTreeModel,
    DecisionTreeVisualizer,
    decision_tree,
)
from animora.ml.classic.kmeans import (
    KMeansModel,
    KMeansVisualizer,
    kmeans,
)
from animora.ml.classic.linear_regression import (
    LinearRegressionModel,
    LinearRegressionVisualizer,
    linear_regression,
)
from animora.ml.classic.logistic_regression import (
    LogisticRegressionModel,
    LogisticRegressionVisualizer,
    logistic_regression,
)
from animora.ml.classic.pca import (
    PCAModel,
    PCAVisualizer,
    pca,
)
from animora.ml.classic.svm import (
    HardMarginSVMModel,
    SVMVisualizer,
    svm,
)

__all__ = [
    "DecisionNode",
    "DecisionTreeModel",
    "DecisionTreeVisualizer",
    "HardMarginSVMModel",
    "KMeansModel",
    "KMeansVisualizer",
    "LinearRegressionModel",
    "LinearRegressionVisualizer",
    "LogisticRegressionModel",
    "LogisticRegressionVisualizer",
    "PCAModel",
    "PCAVisualizer",
    "SVMVisualizer",
    "decision_tree",
    "kmeans",
    "linear_regression",
    "logistic_regression",
    "pca",
    "svm",
]
