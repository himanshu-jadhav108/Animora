"""Animora: High-level declarative animation framework built on Manim.

Democratizing the creation of high-quality educational, technical,
mathematical, and algorithmic animations.
"""

from __future__ import annotations

from animora.algorithms.backtracking import n_queens, n_queens_trace
from animora.algorithms.dynamic_programming import fibonacci_dp, fibonacci_dp_trace
from animora.algorithms.graph_traversal import bfs, bfs_trace, dfs, dfs_trace
from animora.algorithms.pathfinding import (
    a_star,
    a_star_trace,
    dijkstra,
    dijkstra_trace,
)
from animora.algorithms.search import binary_search, binary_search_trace
from animora.algorithms.sorting import (
    bubble_sort,
    bubble_sort_trace,
    insertion_sort,
    insertion_sort_trace,
    merge_sort,
    merge_sort_trace,
    quick_sort,
    quick_sort_trace,
    selection_sort,
    selection_sort_trace,
)
from animora.algorithms.trace import (
    AlgorithmTrace,
    OperationStep,
    OperationTrace,
    OperationType,
)
from animora.components.annotation import Annotation
from animora.components.arrow import Arrow
from animora.components.connector import Connector
from animora.components.group import Group
from animora.components.label import Label
from animora.components.panel import Panel
from animora.components.shape import Shape, ShapeType
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.camera import Camera, MovingCameraScene
from animora.core.component import Component
from animora.core.config import BoundingBox, ComponentConfig
from animora.core.scene import Scene
from animora.datastructures.array import Array, ArrayListModel
from animora.datastructures.bst import BST, BSTModel, BSTNode
from animora.datastructures.graph import Graph, GraphModel
from animora.datastructures.hash_table import HashEntry, HashTable, HashTableChainingModel
from animora.datastructures.heap import Heap, HeapModel
from animora.datastructures.linked_list import LinkedList, LinkedListModel, ListNode
from animora.datastructures.queue import Queue, QueueModel
from animora.datastructures.stack import Stack, StackModel
from animora.datastructures.tree import GenericTreeModel, Tree, TreeNode
from animora.dataviz.axes import Axes
from animora.dataviz.bar_chart import BarChart
from animora.dataviz.histogram import Histogram
from animora.dataviz.line_chart import LineChart
from animora.dataviz.scatter_plot import ScatterPlot
from animora.dataviz.table import Table
from animora.layout.base import BaseLayout, LayoutItem, LayoutResult
from animora.layout.circular import CircularLayout
from animora.layout.collision import (
    CollisionPair,
    check_aabb_overlap,
    compute_aabb_intersection,
    detect_collisions,
    has_collisions,
)
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
from animora.theme.effects import (
    Aurora,
    apply_effect,
)
from animora.theme.presets import (
    CINEMATIC,
    EDUCATIONAL,
    PLAYFUL,
    PRESETS,
    SLOW_MO,
    SMOOTH,
    SNAPPY,
    TimingPreset,
    get_timing_preset,
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

__version__ = "0.2.0a1"

__all__: list[str] = [
    "BST",
    "CINEMATIC",
    "EDUCATIONAL",
    "PLAYFUL",
    "PRESETS",
    "SLOW_MO",
    "SMOOTH",
    "SNAPPY",
    "AlgorithmTrace",
    "Animation",
    "AnimationTiming",
    "Annotation",
    "Array",
    "ArrayListModel",
    "Arrow",
    "Aurora",
    "Axes",
    "BSTModel",
    "BSTNode",
    "BarChart",
    "BaseLayout",
    "BoundingBox",
    "Camera",
    "CircularLayout",
    "CollisionPair",
    "ColorPalette",
    "Component",
    "ComponentConfig",
    "Connector",
    "CornerRadius",
    "Cyberpunk",
    "DefaultTheme",
    "FlowLayout",
    "GenericTreeModel",
    "Graph",
    "GraphLayout",
    "GraphModel",
    "GridLayout",
    "Group",
    "HashEntry",
    "HashTable",
    "HashTableChainingModel",
    "Heap",
    "HeapModel",
    "Histogram",
    "HorizontalLayout",
    "Label",
    "LayoutItem",
    "LayoutResult",
    "LineChart",
    "LinkedList",
    "LinkedListModel",
    "ListNode",
    "ModernDark",
    "Monokai",
    "MovingCameraScene",
    "OperationStep",
    "OperationTrace",
    "OperationType",
    "Panel",
    "PaperLight",
    "Queue",
    "QueueModel",
    "ScatterPlot",
    "Scene",
    "Shape",
    "ShapeType",
    "SpacingScale",
    "Stack",
    "StackModel",
    "StrokeScale",
    "Table",
    "Text",
    "Theme",
    "TimingPreset",
    "Tree",
    "TreeLayout",
    "TreeNode",
    "Typography",
    "VerticalLayout",
    "__version__",
    "a_star",
    "a_star_trace",
    "apply_effect",
    "bfs",
    "bfs_trace",
    "binary_search",
    "binary_search_trace",
    "bubble_sort",
    "bubble_sort_trace",
    "check_aabb_overlap",
    "compute_aabb_intersection",
    "detect_collisions",
    "dfs",
    "dfs_trace",
    "dijkstra",
    "dijkstra_trace",
    "fibonacci_dp",
    "fibonacci_dp_trace",
    "get_active_theme",
    "get_timing_preset",
    "has_collisions",
    "insertion_sort",
    "insertion_sort_trace",
    "merge_sort",
    "merge_sort_trace",
    "n_queens",
    "n_queens_trace",
    "quick_sort",
    "quick_sort_trace",
    "selection_sort",
    "selection_sort_trace",
    "set_active_theme",
    "use_theme",
]
