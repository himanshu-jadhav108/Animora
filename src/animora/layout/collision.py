"""Bounding box collision detection for layout analysis and overlap reporting."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from animora.core.component import Component
from animora.core.config import BoundingBox


@dataclass(frozen=True)
class CollisionPair:
    """Represents a detected collision between two components or bounding boxes."""

    first: Component | BoundingBox
    second: Component | BoundingBox
    overlap_box: BoundingBox
    overlap_area: float

    def __repr__(self) -> str:
        first_name = (
            self.first.__class__.__name__ if isinstance(self.first, Component) else "BoundingBox"
        )
        second_name = (
            self.second.__class__.__name__ if isinstance(self.second, Component) else "BoundingBox"
        )
        return (
            f"<CollisionPair {first_name} <-> {second_name} overlap_area={self.overlap_area:.4f}>"
        )


def check_aabb_overlap(
    box1: BoundingBox,
    box2: BoundingBox,
    tolerance: float = 1e-5,
) -> bool:
    """Check whether two 2D/3D axis-aligned bounding boxes overlap.

    Parameters:
        box1: First bounding box.
        box2: Second bounding box.
        tolerance: Minimum overlap depth to count as collision
            (avoids border-touching false positives).

    Returns:
        True if bounding boxes strictly intersect beyond tolerance, False otherwise.
    """
    # X-axis separation
    x_separated = (
        box1.max_point[0] <= box2.min_point[0] + tolerance
        or box2.max_point[0] <= box1.min_point[0] + tolerance
    )
    if x_separated:
        return False

    # Y-axis separation
    y_separated = (
        box1.max_point[1] <= box2.min_point[1] + tolerance
        or box2.max_point[1] <= box1.min_point[1] + tolerance
    )
    return not y_separated


def compute_aabb_intersection(
    box1: BoundingBox,
    box2: BoundingBox,
    tolerance: float = 1e-5,
) -> BoundingBox | None:
    """Compute the intersection bounding box between two overlapping AABBs.

    Returns:
        BoundingBox representing the intersection volume, or None if no overlap exists.
    """
    if not check_aabb_overlap(box1, box2, tolerance=tolerance):
        return None

    min_x = max(box1.min_point[0], box2.min_point[0])
    max_x = min(box1.max_point[0], box2.max_point[0])
    min_y = max(box1.min_point[1], box2.min_point[1])
    max_y = min(box1.max_point[1], box2.max_point[1])
    min_z = max(box1.min_point[2], box2.min_point[2])
    max_z = min(box1.max_point[2], box2.max_point[2])

    return BoundingBox(
        min_point=(float(min_x), float(min_y), float(min_z)),
        max_point=(float(max_x), float(max_y), float(max_z)),
    )


def detect_collisions(
    items: Sequence[Component | BoundingBox],
    tolerance: float = 1e-5,
) -> list[CollisionPair]:
    """Identify all pairwise overlapping bounding boxes among a collection of components.

    Guarantees lazy-build safety by realizing underlying mobjects before querying bounds.

    Parameters:
        items: Sequence of Component instances or BoundingBox objects.
        tolerance: Minimum intersection buffer required to classify as an overlap.

    Returns:
        List of CollisionPair objects containing overlapping items and intersection metrics.
    """
    resolved_boxes: list[tuple[Component | BoundingBox, BoundingBox]] = []

    for item in items:
        if isinstance(item, Component):
            # Ensure component mobject is realized (BUG-001 safe)
            _ = item.manim_object
            resolved_boxes.append((item, item.bounding_box))
        elif isinstance(item, BoundingBox):
            resolved_boxes.append((item, item))
        else:
            raise TypeError(f"Expected Component or BoundingBox, got {type(item).__name__}")

    collisions: list[CollisionPair] = []
    n = len(resolved_boxes)

    for i in range(n):
        item_i, box_i = resolved_boxes[i]
        for j in range(i + 1, n):
            item_j, box_j = resolved_boxes[j]
            intersection = compute_aabb_intersection(box_i, box_j, tolerance=tolerance)
            if intersection is not None:
                area = intersection.width * intersection.height
                collisions.append(
                    CollisionPair(
                        first=item_i,
                        second=item_j,
                        overlap_box=intersection,
                        overlap_area=area,
                    )
                )

    return collisions


def has_collisions(
    items: Sequence[Component | BoundingBox],
    tolerance: float = 1e-5,
) -> bool:
    """Quick boolean test for existence of any collisions (short-circuiting)."""
    resolved_boxes: list[BoundingBox] = []
    for item in items:
        if isinstance(item, Component):
            _ = item.manim_object
            resolved_boxes.append(item.bounding_box)
        elif isinstance(item, BoundingBox):
            resolved_boxes.append(item)
        else:
            raise TypeError(f"Expected Component or BoundingBox, got {type(item).__name__}")

    n = len(resolved_boxes)
    for i in range(n):
        for j in range(i + 1, n):
            if check_aabb_overlap(resolved_boxes[i], resolved_boxes[j], tolerance=tolerance):
                return True
    return False


__all__ = [
    "CollisionPair",
    "check_aabb_overlap",
    "compute_aabb_intersection",
    "detect_collisions",
    "has_collisions",
]
