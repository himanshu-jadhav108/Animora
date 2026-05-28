"""Circular layout solver arranging items radially around a circle."""

from __future__ import annotations

import math
from typing import Any, Sequence

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class CircularLayout(BaseLayout):
    """Arranges layout items evenly around a circle or arc.

    Example:
    ```python
    layout = CircularLayout(radius=2.5, clockwise=True)
    result = layout.solve(items)
    ```
    """

    def __init__(
        self,
        radius: float | None = None,
        start_angle: float = math.pi / 2.0,
        end_angle: float | None = None,
        clockwise: bool = True,
        center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> None:
        self.radius = radius
        self.start_angle = float(start_angle)
        self.end_angle = end_angle
        self.clockwise = clockwise
        self.center = center

    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        if not items:
            return LayoutResult(positions={}, total_width=0.0, total_height=0.0)

        n = len(items)
        if n == 1:
            return LayoutResult(
                positions={items[0].id: self.center},
                total_width=items[0].width,
                total_height=items[0].height,
            )

        # 1. Determine or auto-compute radius
        if self.radius is not None:
            r = float(self.radius)
        else:
            # Estimate radius so items don't collide
            max_dim = max(max(item.width, item.height) for item in items)
            perimeter_needed = n * (max_dim * 1.5)
            r = max(1.5, perimeter_needed / (2.0 * math.pi))

        # 2. Angle step
        direction_sign = -1.0 if self.clockwise else 1.0
        if self.end_angle is not None:
            total_sweep = self.end_angle - self.start_angle
            angle_step = total_sweep / max(1, n - 1)
        else:
            angle_step = (2.0 * math.pi / n) * direction_sign

        positions: dict[str, tuple[float, float, float]] = {}
        for idx, item in enumerate(items):
            theta = self.start_angle + (idx * angle_step)
            x = self.center[0] + (r * math.cos(theta))
            y = self.center[1] + (r * math.sin(theta))
            z = self.center[2]
            positions[item.id] = (x, y, z)

        total_dim = 2.0 * r
        return LayoutResult(
            positions=positions,
            total_width=total_dim,
            total_height=total_dim,
        )


__all__ = [
    "CircularLayout",
]
