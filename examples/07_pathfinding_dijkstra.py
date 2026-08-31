"""Example 07: Pathfinding Algorithm Visualization (Dijkstra on Graph)."""

from __future__ import annotations

from animora.algorithms import dijkstra
from animora.core import Scene
from animora.datastructures import Graph
from animora.theme import ModernDark, use_theme


class DijkstraPathfindingScene(Scene):
    """Demonstrates Dijkstra shortest path algorithm visualization on a Graph component."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Construct Graph
            g = Graph(
                nodes=["A", "B", "C", "D"],
                edges=[("A", "B"), ("B", "D"), ("A", "C"), ("C", "D")],
            )
            self.play(g.animate_create(run_time=0.8))
            self.wait(0.3)

            # 2. Run Dijkstra animations
            dijkstra_anims = dijkstra(g, start="A", target="D", run_time=0.4)
            for anim in dijkstra_anims:
                self.play(anim)
            self.wait(0.5)


if __name__ == "__main__":
    import manim

    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = DijkstraPathfindingScene()
        scene.render()
