"""Visual primitive components for Animora.

Includes foundational primitives: Text, Shape, Arrow, Connector, Group, and Panel.
"""

from __future__ import annotations

from animora.components.arrow import Arrow
from animora.components.connector import Connector
from animora.components.group import Group
from animora.components.panel import Panel
from animora.components.shape import Shape, ShapeType
from animora.components.text import Text

__all__: list[str] = [
    "Arrow",
    "Connector",
    "Group",
    "Panel",
    "Shape",
    "ShapeType",
    "Text",
]
