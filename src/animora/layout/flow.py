"""Flow layout solver for step-based sequences and wrapped pipeline diagrams."""

from __future__ import annotations

from typing import Any, Sequence

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class FlowLayout(BaseLayout):
    """Arranges layout items in a flowing sequential chain with optional line wrapping.

    Ideal for execution pipelines, step-by-step state diagrams, and flowcharts.

    Example:
    ```python
    layout = FlowLayout(direction="right", spacing=0.8, wrap_after=4)
    result = layout.solve(items)
    ```
    """

    def __init__(
        self,
        direction: str = "right",
        spacing: float = 0.8,
        line_spacing: float = 1.2,
        wrap_after: int | None = None,
        center_origin: bool = True,
    ) -> None:
        self.direction = direction.lower()
        self.spacing = float(spacing)
        self.line_spacing = float(line_spacing)
        self.wrap_after = wrap_after
        self.center_origin = center_origin

    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        if not items:
            return LayoutResult(positions={}, total_width=0.0, total_height=0.0)

        wrap = self.wrap_after or len(items)
        positions: dict[str, tuple[float, float, float]] = {}

        raw_coords: list[tuple[float, float]] = []

        if self.direction in ("right", "left"):
            # Horizontal rows
            current_x = 0.0
            current_y = 0.0

            for idx, item in enumerate(items):
                if idx > 0 and idx % wrap == 0:
                    current_x = 0.0
                    current_y -= self.line_spacing + max(it.height for it in items)

                item_x = current_x + (item.width / 2.0)
                item_y = current_y

                raw_coords.append((item_x, item_y))
                current_x += item.width + self.spacing

        else:
            # Vertical columns ("down", "up")
            current_x = 0.0
            current_y = 0.0

            for idx, item in enumerate(items):
                if idx > 0 and idx % wrap == 0:
                    current_y = 0.0
                    current_x += self.line_spacing + max(it.width for it in items)

                item_x = current_x
                item_y = current_y - (item.height / 2.0)

                raw_coords.append((item_x, item_y))
                current_y -= item.height + self.spacing

        # Center calculation
        xs = [c[0] for c in raw_coords]
        ys = [c[1] for c in raw_coords]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        total_w = max_x - min_x
        total_h = max_y - min_y

        offset_x = (min_x + max_x) / 2.0 if self.center_origin else 0.0
        offset_y = (min_y + max_y) / 2.0 if self.center_origin else 0.0

        for item, (rx, ry) in zip(items, raw_coords):
            positions[item.id] = (rx - offset_x, ry - offset_y, 0.0)

        return LayoutResult(
            positions=positions,
            total_width=total_w,
            total_height=total_h,
        )


__all__ = [
    "FlowLayout",
]
