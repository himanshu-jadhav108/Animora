"""Animora AI/ML visualization module for surfaces, vector fields, grids, and optimization."""

from __future__ import annotations

from animora.ml.base import MLComponent, MLTrace, MLTraceStep
from animora.ml.optimization.gradient_descent import (
    GradientDescentModel,
    GradientDescentVisualizer,
    gradient_descent,
)
from animora.ml.surface_plot import SurfacePlot
from animora.ml.tensor_grid import TensorGrid
from animora.ml.vector_field import VectorField

__all__ = [
    "GradientDescentModel",
    "GradientDescentVisualizer",
    "MLComponent",
    "MLTrace",
    "MLTraceStep",
    "SurfacePlot",
    "TensorGrid",
    "VectorField",
    "gradient_descent",
]
