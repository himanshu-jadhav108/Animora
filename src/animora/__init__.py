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
from animora.dataviz.axes import Axes
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.histogram import Histogram
from animora.dataviz.line_chart import LineChart
from animora.dataviz.scatter_plot import ScatterPlot
from animora.dataviz.table import Table
from animora.layout.base import BaseLayout, LayoutItem, LayoutResult
from animora.layout.circular import CircularLayout
from animora.layout.flow import FlowLayout
from animora.layout.graph import GraphLayout
from animora.layout.grid import GridLayout
from animora.layout.horizontal import HorizontalLayout
from animora.layout.tree import TreeLayout
from animora.layout.vertical import VerticalLayout
from animora.theme.builtin import (
    Cyberpunk,
    DefaultTheme,
    ModernDark,
    Monokai,
    PaperLight,
)
from animora.theme.context import (
    get_active_theme,
    set_active_theme,
    use_theme,
)
from animora.theme.theme import (
    AnimationTiming,
    ColorPalette,
    CornerRadius,
    SpacingScale,
    StrokeScale,
    Theme,
    Typography,
)

__version__ = "0.1.0.dev0"

__all__: list[str] = [
    "Animation",
    "AnimationTiming",
    "Arrow",
    "Axes",
    "BarChart",
    "BaseLayout",
    "BoundingBox",
    "CircularLayout",
    "ColorPalette",
    "Component",
    "ComponentConfig",
    "Connector",
    "CornerRadius",
    "Cyberpunk",
    "DefaultTheme",
    "FlowLayout",
    "GraphLayout",
    "GridLayout",
    "Group",
    "Histogram",
    "HorizontalLayout",
    "Label",
    "LayoutItem",
    "LayoutResult",
    "LineChart",
    "ModernDark",
    "Monokai",
    "Panel",
    "PaperLight",
    "ScatterPlot",
    "Scene",
    "Shape",
    "ShapeType",
    "SpacingScale",
    "StrokeScale",
    "Table",
    "Text",
    "Theme",
    "TreeLayout",
    "Typography",
    "VerticalLayout",
    "__version__",
    "get_active_theme",
    "set_active_theme",
    "use_theme",
]
