"""Integration test verifying Group.arrange() with multiple layout solvers in Manim."""

from __future__ import annotations

import manim
import pytest

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.scene import Scene
from animora.layout.circular import CircularLayout
from animora.layout.grid import GridLayout
from animora.layout.horizontal import HorizontalLayout
from animora.layout.tree import TreeLayout


def test_group_arrange_grid_layout() -> None:
    """Verify Group.arrange with GridLayout correctly repositions children."""
    circles = [Shape.circle(radius=0.4) for _ in range(6)]
    grp = Group(*circles)

    grp.arrange(GridLayout(columns=3, col_spacing=0.5, row_spacing=0.5))

    # Check that children have distinct positions
    centers = [c.center for c in circles]
    unique_x = {round(float(c[0]), 2) for c in centers}
    unique_y = {round(float(c[1]), 2) for c in centers}

    assert len(unique_x) == 3  # 3 columns
    assert len(unique_y) == 2  # 2 rows


def test_group_arrange_tree_layout() -> None:
    """Verify Group.arrange with TreeLayout."""
    nodes = [Shape.circle(radius=0.3) for _ in range(3)]
    grp = Group(*nodes)

    # 0 is root, 1 and 2 are children
    edges = [("0", "1"), ("0", "2")]
    grp.arrange(TreeLayout(edges=edges, root_id="0", level_spacing=1.5, node_spacing=1.0))

    # Root (0) must have higher Y coordinate than children (1, 2)
    assert nodes[0].center[1] > nodes[1].center[1]
    assert pytest.approx(nodes[1].center[1], abs=1e-2) == nodes[2].center[1]


class LayoutsDemoScene(Scene):
    """Rendered integration scene testing multiple layout arrangements."""

    def construct(self) -> None:
        # 1. Grid layout of shapes
        grid_nodes = [Shape.circle(radius=0.3, fill_color="#38BDF8") for _ in range(4)]
        grid_group = Group(*grid_nodes)
        grid_group.arrange(GridLayout(columns=2, col_spacing=0.4, row_spacing=0.4))
        grid_group.move_to([-3.0, 0.0, 0.0])

        # 2. Circular layout of shapes
        ring_nodes = [Shape.circle(radius=0.25, fill_color="#10B981") for _ in range(5)]
        ring_group = Group(*ring_nodes)
        ring_group.arrange(CircularLayout(radius=1.2))
        ring_group.move_to([3.0, 0.0, 0.0])

        self.play(grid_group.animate_fade_in(run_time=0.1))
        self.play(ring_group.animate_create(run_time=0.1))


def test_layouts_scene_render_end_to_end() -> None:
    """Verify combined layout scene renders cleanly in Manim dry_run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = LayoutsDemoScene()
        scene.render()
        assert len(scene.mobjects) >= 2
