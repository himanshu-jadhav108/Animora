"""Horizontal layout solver arranging items from left to right."""

from __future__ import annotations

from typing import Any, Sequence

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class HorizontalLayout(BaseLayout):
    """Arranges layout items in a horizontal line from left to right.

    Example:
    ```python
    layout = HorizontalLayout(spacing=0.5, alignment="center")
    result = layout.solve(items)
    ```
    """

    def __init__(
        self,
        spacing: float = 0.5,
        alignment: str = "center",
        center_origin: bool = True,
    ) -> None:
        self.spacing = float(spacing)
        self.alignment = alignment.lower()
        self.center_origin = center_origin

    def solve(
        self,
        items: Sequence[LayoutItem],
        **kwargs: Any,
    ) -> LayoutResult:
        if not items:
            return LayoutResult(positions={}, total_width=0.0, total_height=0.0)

        # 1. Calculate total width and max height
        total_item_widths = sum(item.width for item in items)
        total_spacings = self.spacing * max(0, len(items) - 1)
        total_width = total_item_widths + total_spacings
        max_height = max(item.height for item in items)

        # 2. Determine initial X offset
        current_x = -total_width / 2.0 if self.center_origin else 0.0

        positions: dict[str, tuple[float, float, float]] = {}
        for item in items:
            item_center_x = current_x + (item.width / 2.0)

            # Alignment along Y axis
            if self.alignment == "top":
                item_center_y = (max_height / 2.0) - (item.height / 2.0)
            elif self.alignment == "bottom":
                item_center_y = (-max_height / 2.0) + (item.height / 2.0)
            else:  # "center"
                item_center_y = 0.0

            positions[item.id] = (item_center_x, item_center_y, 0.0)
            current_x += item.width + self.spacing

        return LayoutResult(
            positions=positions,
            total_width=total_width,
            total_height=max_height,
        )


__all__ = [
    "HorizontalLayout",
]
