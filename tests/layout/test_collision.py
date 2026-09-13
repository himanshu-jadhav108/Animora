"""Unit tests for layout collision detection."""

from __future__ import annotations

import pytest

from animora.components.annotation import Annotation
from animora.components.panel import Panel
from animora.components.shape import Shape, ShapeType
from animora.core.config import BoundingBox
from animora.datastructures.tree import Tree
from animora.layout.collision import (
    check_aabb_overlap,
    compute_aabb_intersection,
    detect_collisions,
    has_collisions,
)

# ---------------------------------------------------------------------------
# Edge Cases: Primitive BoundingBox tests
# ---------------------------------------------------------------------------


def test_aabb_overlap_identical_boxes() -> None:
    """Identical bounding boxes must overlap with area equal to full box."""
    box1 = BoundingBox(min_point=(0.0, 0.0, 0.0), max_point=(2.0, 2.0, 0.0))
    box2 = BoundingBox(min_point=(0.0, 0.0, 0.0), max_point=(2.0, 2.0, 0.0))

    assert check_aabb_overlap(box1, box2) is True
    intersection = compute_aabb_intersection(box1, box2)
    assert intersection is not None
    assert pytest.approx(intersection.width) == 2.0
    assert pytest.approx(intersection.height) == 2.0
    assert pytest.approx(intersection.width * intersection.height) == 4.0


def test_aabb_overlap_touching_borders() -> None:
    """Boxes touching exactly at borders should not count as overlapping (tolerance check)."""
    box1 = BoundingBox(min_point=(0.0, 0.0, 0.0), max_point=(1.0, 1.0, 0.0))
    # box2 touches right edge of box1
    box2 = BoundingBox(min_point=(1.0, 0.0, 0.0), max_point=(2.0, 1.0, 0.0))

    assert check_aabb_overlap(box1, box2) is False
    assert compute_aabb_intersection(box1, box2) is None


def test_aabb_overlap_contained_box() -> None:
    """An inner box contained inside an outer box must overlap with area equal to inner box."""
    outer = BoundingBox(min_point=(-2.0, -2.0, 0.0), max_point=(2.0, 2.0, 0.0))
    inner = BoundingBox(min_point=(-0.5, -0.5, 0.0), max_point=(0.5, 0.5, 0.0))

    assert check_aabb_overlap(outer, inner) is True
    intersection = compute_aabb_intersection(outer, inner)
    assert intersection is not None
    assert pytest.approx(intersection.min_point) == inner.min_point
    assert pytest.approx(intersection.max_point) == inner.max_point
    assert pytest.approx(intersection.width * intersection.height) == 1.0


def test_detect_collisions_invalid_type() -> None:
    """detect_collisions raises TypeError when given unsupported types."""
    with pytest.raises(TypeError, match="Expected Component or BoundingBox"):
        detect_collisions(["not_a_component"])  # type: ignore[list-item]

    with pytest.raises(TypeError, match="Expected Component or BoundingBox"):
        has_collisions([123])  # type: ignore[list-item]


# ---------------------------------------------------------------------------
# Scenario A: Dense GridLayout with intentionally tight/overlapping spacing
# ---------------------------------------------------------------------------


def test_scenario_a_dense_grid_collision() -> None:
    """Dense/overlapping grid layout items trigger collision detection."""
    # Create 4 panels positioned with overlapping coordinates (spacing smaller than panel size)
    p1 = Panel(title="P1", width=2.0, height=2.0)
    p2 = Panel(title="P2", width=2.0, height=2.0)

    # Move p2 to overlap significantly with p1
    _ = p1.manim_object
    _ = p2.manim_object
    p1.manim_object.move_to([0.0, 0.0, 0.0])
    p2.manim_object.move_to([1.0, 0.5, 0.0])  # Overlaps in both X and Y

    collisions = detect_collisions([p1, p2])
    assert len(collisions) == 1
    pair = collisions[0]
    assert pair.first is p1
    assert pair.second is p2
    assert pair.overlap_area > 0.0
    assert has_collisions([p1, p2]) is True


# ---------------------------------------------------------------------------
# Scenario B: TreeLayout with an annotation attached to a node
# ---------------------------------------------------------------------------


def test_scenario_b_tree_node_annotation_collision() -> None:
    """Annotation attached to a tree node extending into sibling node space is detected."""
    tree = Tree(root_value="root")
    tree.model.insert_child("root", "left")
    tree.model.insert_child("root", "right")
    _ = tree.manim_object

    left_node = tree.get_node("left")
    right_node = tree.get_node("right")

    # Attach an annotation on left node pointing rightwards toward right node
    annotation = Annotation(left_node, text="Very Long Callout Label", direction=[1.0, 0.0, 0.0])
    _ = annotation.manim_object

    # Manually position annotation to intentionally overlap with right node
    right_center = right_node.manim_object.get_center()
    annotation.manim_object.move_to(right_center)

    collisions = detect_collisions([left_node, right_node, annotation])
    overlap_detected = any(
        (c.first is annotation and c.second is right_node)
        or (c.first is right_node and c.second is annotation)
        for c in collisions
    )
    assert overlap_detected is True
    assert has_collisions([left_node, right_node, annotation]) is True


# ---------------------------------------------------------------------------
# Scenario C: Negative-case control (well-spaced layout with 0 collisions)
# ---------------------------------------------------------------------------


def test_scenario_c_negative_control_zero_collisions() -> None:
    """Well-spaced components yield zero collisions."""
    s1 = Shape(shape_type=ShapeType.RECTANGLE, width=1.0, height=1.0)
    s2 = Shape(shape_type=ShapeType.RECTANGLE, width=1.0, height=1.0)
    s3 = Shape(shape_type=ShapeType.RECTANGLE, width=1.0, height=1.0)

    _ = s1.manim_object
    _ = s2.manim_object
    _ = s3.manim_object

    # Position them far apart along the X axis
    s1.manim_object.move_to([-4.0, 0.0, 0.0])
    s2.manim_object.move_to([0.0, 0.0, 0.0])
    s3.manim_object.move_to([4.0, 0.0, 0.0])

    assert has_collisions([s1, s2, s3]) is False
    assert detect_collisions([s1, s2, s3]) == []


def test_lazy_build_safety_in_collision_detection() -> None:
    """Components whose manim_object hasn't been accessed yet are safely realized."""
    s1 = Shape(shape_type=ShapeType.CIRCLE, width=1.0, height=1.0)
    s2 = Shape(shape_type=ShapeType.CIRCLE, width=1.0, height=1.0)

    assert s1._mobject is None
    assert s2._mobject is None

    # detect_collisions should trigger realization without error
    collisions = detect_collisions([s1, s2])
    assert s1._mobject is not None
    assert s2._mobject is not None
    # Since both are at origin by default, they collide
    assert len(collisions) == 1
