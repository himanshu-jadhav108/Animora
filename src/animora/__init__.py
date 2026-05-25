"""Animora: High-level declarative animation framework built on Manim.

Democratizing the creation of high-quality educational, technical,
mathematical, and algorithmic animations.
"""

from __future__ import annotations

from animora.components.label import Label
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import BoundingBox, ComponentConfig
from animora.core.scene import Scene

__version__ = "0.1.0.dev0"

__all__: list[str] = [
    "Animation",
    "BoundingBox",
    "Component",
    "ComponentConfig",
    "Label",
    "Scene",
    "__version__",
]
