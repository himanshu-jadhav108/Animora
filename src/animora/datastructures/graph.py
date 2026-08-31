"""Graph data structure component positioned via Phase 4 GraphLayout."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim

from animora.components.arrow import Arrow
from animora.components.connector import Connector
from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.layout.graph import GraphLayout
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


# -----------------------------------------------------------------------------
# 1. Pure Python Data Model (No Manim Dependency)
# -----------------------------------------------------------------------------
class GraphModel:
    """Pure Python Graph model supporting adjacency and state queries."""

    def __init__(self, directed: bool = False) -> None:
        self.directed: bool = directed
        self.adj: dict[Any, list[tuple[Any, float | None]]] = {}

    def add_node(self, node: Any) -> None:
        """Add node if not present."""
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u: Any, v: Any, weight: float | None = None) -> None:
        """Add edge (u, v) with optional weight."""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def remove_edge(self, u: Any, v: Any) -> bool:
        """Remove edge (u, v). Return True if removed."""
        if u not in self.adj:
            return False
        orig_len = len(self.adj[u])
        self.adj[u] = [edge for edge in self.adj[u] if edge[0] != v]
        removed = len(self.adj[u]) < orig_len

        if not self.directed and v in self.adj:
            self.adj[v] = [edge for edge in self.adj[v] if edge[0] != u]

        return removed

    def neighbors(self, u: Any) -> list[Any]:
        """Return list of neighboring node identifiers."""
        return [neighbor for neighbor, _ in self.adj.get(u, [])]

    def nodes(self) -> list[Any]:
        return list(self.adj.keys())

    def edges(self) -> list[tuple[Any, Any]]:
        """Return list of distinct edges."""
        seen: set[tuple[Any, Any]] = set()
        result: list[tuple[Any, Any]] = []

        for u, nbrs in self.adj.items():
            for v, _ in nbrs:
                if self.directed:
                    result.append((u, v))
                else:
                    pair = (min(str(u), str(v)), max(str(u), str(v)))
                    if pair not in seen:
                        seen.add(pair)
                        result.append((u, v))
        return result


# -----------------------------------------------------------------------------
# 2. Visual Component & Animation Generation
# -----------------------------------------------------------------------------
class Graph(Component):
    """Visual Graph data structure component positioned via GraphLayout.

    Exposes state-visualization primitives for algorithmic highlights
    (e.g., mark visited, highlight edge, highlight node).

    Example:
    ```python
    g = Graph(directed=False)
    g.model.add_edge("A", "B")
    g.model.add_edge("B", "C")
    g.model.add_edge("C", "A")
    scene.play(g.animate_highlight_node("B"))
    scene.play(g.animate_highlight_edge("A", "B"))
    ```
    """

    def __init__(
        self,
        nodes: Sequence[Any] | None = None,
        edges: Sequence[tuple[Any, Any]] | None = None,
        *,
        directed: bool = False,
        node_radius: float = 0.4,
        layout_algorithm: str = "spring",
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._model = GraphModel(directed=directed)
        for n in nodes or []:
            self._model.add_node(n)
        for u, v in edges or []:
            self._model.add_edge(u, v)

        self._node_radius = float(node_radius)
        self._layout_algorithm = layout_algorithm

        self._node_map: dict[Any, Group] = {}
        self._edge_map: dict[tuple[Any, Any], Connector] = {}
        super().__init__(config=config, **kwargs)

    @property
    def model(self) -> GraphModel:
        return self._model

    def _build_mobject(self) -> manim.Mobject:
        """Build graph nodes and edges using GraphLayout positioning."""
        active_theme = get_active_theme()

        self._node_map = {}
        self._edge_map = {}
        all_mobjects: list[manim.Mobject] = []

        all_nodes = self._model.nodes()
        if not all_nodes:
            return manim.VGroup()

        # 1. Build node visual groups
        node_components: list[Group] = []
        for n in all_nodes:
            circle = Shape.circle(
                radius=self._node_radius,
                fill_color=active_theme.colors.surface,
                fill_opacity=0.9,
                stroke_color=active_theme.colors.primary,
                stroke_width=active_theme.strokes.regular,
            )
            txt = Text(
                str(n),
                font_size=active_theme.typography.font_size_sm,
                color=active_theme.colors.text,
            )
            grp = Group(circle, txt)
            self._node_map[n] = grp
            node_components.append(grp)

        # 2. Position via Phase 4 GraphLayout
        edge_tuples = [(str(u), str(v)) for u, v in self._model.edges()]
        layout = GraphLayout(
            edges=edge_tuples,
            algorithm=self._layout_algorithm,
            scale=3.0,
        )

        container = Group(*node_components)
        container.arrange(layout)

        for grp in node_components:
            all_mobjects.append(grp.manim_object)

        # 3. Create edges
        for u, v in self._model.edges():
            grp_u = self._node_map[u]
            grp_v = self._node_map[v]

            if self._model.directed:
                conn: Connector = Arrow(
                    start=grp_u,
                    end=grp_v,
                    buff=self._node_radius + 0.05,
                    stroke_color=active_theme.colors.border,
                )
            else:
                conn = Connector(
                    start=grp_u,
                    end=grp_v,
                    stroke_color=active_theme.colors.border,
                    stroke_width=active_theme.strokes.regular,
                )

            self._edge_map[(u, v)] = conn
            if not self._model.directed:
                self._edge_map[(v, u)] = conn

            all_mobjects.append(conn.manim_object)

        return manim.VGroup(*all_mobjects)

    # -------------------------------------------------------------------------
    # State-Visualization Primitives for Algorithms (Phase 8 Foundation)
    # -------------------------------------------------------------------------
    def animate_highlight_node(
        self,
        node: Any,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Highlight a node."""
        active_theme = get_active_theme()
        col = color or active_theme.colors.accent
        duration = run_time or active_theme.timing.fast

        target = self._node_map[node]
        return Animation(
            component=target,
            manim_animation=manim.Indicate(target.manim_object, color=col),
            run_time=duration,
            name=f"highlight_node({node})",
        )

    def animate_mark_visited(
        self,
        node: Any,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Mark a node as visited during traversal."""
        active_theme = get_active_theme()
        col = color or active_theme.colors.success
        duration = run_time or active_theme.timing.normal

        target = self._node_map[node]
        circle = target.children[0]
        return Animation(
            component=target,
            manim_animation=circle.manim_object.animate.set_color(col),
            run_time=duration,
            name=f"mark_visited({node})",
        )

    def animate_highlight_edge(
        self,
        u: Any,
        v: Any,
        color: str | None = None,
        run_time: float | None = None,
    ) -> Animation:
        """Highlight an edge between node u and node v."""
        active_theme = get_active_theme()
        col = color or active_theme.colors.accent
        duration = run_time or active_theme.timing.normal

        edge = self._edge_map.get((u, v))
        if edge is None:
            raise KeyError(f"Edge ({u}, {v}) not found in graph")

        return Animation(
            component=edge,
            manim_animation=manim.Indicate(edge.manim_object, color=col),
            run_time=duration,
            name=f"highlight_edge({u}, {v})",
        )


__all__ = [
    "Graph",
    "GraphModel",
]
