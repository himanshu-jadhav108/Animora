"""Pure layout and geometric solver engine for Animora.

Responsible for computing spatial coordinates, bounding boxes, and alignment
vectors for collections of visual elements. Contains algorithms for linear,
grid, circular, tree, and graph layouts with zero rendering dependencies.
"""

from __future__ import annotations

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult
from animora.layout.circular import CircularLayout
from animora.layout.flow import FlowLayout
from animora.layout.graph import GraphLayout
from animora.layout.grid import GridLayout
from animora.layout.horizontal import HorizontalLayout
from animora.layout.tree import TreeLayout
from animora.layout.vertical import VerticalLayout

__all__: list[str] = [
    "BaseLayout",
    "CircularLayout",
    "FlowLayout",
    "GraphLayout",
    "GridLayout",
    "HorizontalLayout",
    "LayoutItem",
    "LayoutResult",
    "TreeLayout",
    "VerticalLayout",
]
