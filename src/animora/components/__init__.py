"""Component abstractions and concrete visual elements for Animora.

Implements all user-facing domain components, providing intuitive construction,
state representations, and semantic animation methods. Organizes components into
visual primitives, data visualizations, and computer science data structures.
"""

from __future__ import annotations

from animora.components.arrow import Arrow
from animora.components.connector import Connector
from animora.components.group import Group
from animora.components.label import Label
from animora.components.panel import Panel
from animora.components.shape import Shape, ShapeType
from animora.components.text import Text

__all__: list[str] = [
    "Arrow",
    "Connector",
    "Group",
    "Label",
    "Panel",
    "Shape",
    "ShapeType",
    "Text",
]
