"""Graph layout solver computing 2D/3D node coordinates using network topologies."""

from __future__ import annotations

import math
from typing import Any, Sequence
import networkx as nx

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class GraphLayout(BaseLayout):
    """Computes spatial coordinates for graph nodes and topologies.

    Supports spring (force-directed), circular, and spectral layout algorithms
    powered by NetworkX.

    Note on Limitations:
    Graph layouts use heuristic optimization (Fruchterman-Reingold spring or
    circular embedding) with a deterministic seed to ensure reproducible positioning.
    Future phases can introduce dynamic physics simulations.

    Example:
    ```python
    layout = GraphLayout(
        edges=[("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")],
        algorithm="spring",
        scale=2.5,
    )
    result = layout.solve(items)
    ```
    """

    def __init__(
        self,
        edges: Sequence[tuple[str, str]] | None = None,
        algorithm: str = "spring",
        scale: float = 2.5,
        iterations: int = 50,
        seed: int = 42,
    ) -> None:
        self.edges = edges or []
        self.algorithm = algorithm.lower()
        self.scale = float(scale)
        self.iterations = int(iterations)
        self.seed = seed

    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        if not items:
            return LayoutResult(positions={}, total_width=0.0, total_height=0.0)

        # Allow passing edges dynamically
        edges = kwargs.get("edges", self.edges)
        algorithm = kwargs.get("algorithm", self.algorithm).lower()
        scale = kwargs.get("scale", self.scale)

        node_ids = [item.id for item in items]
        g = nx.Graph()
        g.add_nodes_from(node_ids)
        if edges:
            g.add_edges_from(edges)

        # Run NetworkX layout
        if algorithm == "circular" or len(node_ids) <= 2:
            raw_pos = nx.circular_layout(g, scale=scale)
        elif algorithm == "kamada_kawai" and nx.is_connected(g):
            raw_pos = nx.kamada_kawai_layout(g, scale=scale)
        else:
            # Default to spring (Fruchterman-Reingold)
            raw_pos = nx.spring_layout(
                g,
                scale=scale,
                iterations=self.iterations,
                seed=self.seed,
            )

        positions: dict[str, tuple[float, float, float]] = {}
        for node_id in node_ids:
            if node_id in raw_pos:
                p = raw_pos[node_id]
                positions[node_id] = (float(p[0]), float(p[1]), 0.0)
            else:
                positions[node_id] = (0.0, 0.0, 0.0)

        total_dim = 2.0 * scale
        return LayoutResult(
            positions=positions,
            total_width=total_dim,
            total_height=total_dim,
        )


__all__ = [
    "GraphLayout",
]
