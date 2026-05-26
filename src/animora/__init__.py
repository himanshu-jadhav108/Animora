"""Animora: High-level declarative animation framework built on Manim.

Democratizing the creation of high-quality educational, technical,
mathematical, and algorithmic animations.
"""

from __future__ import annotations

from animora.components.arrow import Arrow
from animora.components.connector import Connector
from animora.components.group import Group
from animora.components.label import Label
from animora.components.panel import Panel
from animora.components.shape import Shape, ShapeType
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import BoundingBox, ComponentConfig
from animora.core.scene import Scene

__version__ = "0.1.0.dev0"

__all__: list[str] = [
    "Animation",
    "Arrow",
    "BoundingBox",
    "Component",
    "ComponentConfig",
    "Connector",
    "Group",
    "Label",
    "Panel",
    "Scene",
    "Shape",
    "ShapeType",
    "Text",
    "__version__",
]
