"""Core abstraction layer for Animora.

Defines the foundational base classes and runtime lifecycle that connect
Animora's declarative world to Manim's rendering pipeline. It provides
the base Component class, the base Scene wrapper, the AnimationBuilder
interface, and the internal registry that manages plugin extensions and
global engine configuration.
"""

from __future__ import annotations

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import BoundingBox, ComponentConfig
from animora.core.scene import Scene

__all__: list[str] = [
    "Animation",
    "BoundingBox",
    "Component",
    "ComponentConfig",
    "Scene",
]
