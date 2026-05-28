"""Vertical layout solver arranging items from top to bottom."""

from __future__ import annotations

from typing import Any, Sequence

from animora.layout.base import BaseLayout, LayoutItem, LayoutResult


class VerticalLayout(BaseLayout):
    """Arranges layout items in a vertical column from top to bottom.

    Example:
    ```python
    layout = VerticalLayout(spacing=0.4, alignment="center")
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

        # 1. Calculate total height and max width
        total_item_heights = sum(item.height for item in items)
        total_spacings = self.spacing * max(0, len(items) - 1)
        total_height = total_item_heights + total_spacings
        max_width = max(item.width for item in items)

        # 2. Determine initial Y offset (top down)
        current_y = total_height / 2.0 if self.center_origin else total_height

        positions: dict[str, tuple[float, float, float]] = {}
        for item in items:
            item_center_y = current_y - (item.height / 2.0)

            # Alignment along X axis
            if self.alignment == "left":
                item_center_x = (-max_width / 2.0) + (item.width / 2.0)
            elif self.alignment == "right":
                item_center_x = (max_width / 2.0) - (item.width / 2.0)
            else:  # "center"
                item_center_x = 0.0

            positions[item.id] = (item_center_x, item_center_y, 0.0)
            current_y -= item.height + self.spacing

        return LayoutResult(
            positions=positions,
            total_width=max_width,
            total_height=total_height,
        )


__all__ = [
    "VerticalLayout",
]
