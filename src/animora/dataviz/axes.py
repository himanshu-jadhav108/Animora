"""Axes component providing coordinate mapping and axis lines for data visualizations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class Axes(Component):
    """A 2D coordinate system mapping data space coordinates to scene space coordinates.

    Provides mathematical transforms (c2p and p2c) and renders axis lines,
    ticks, and numbers styled via the active theme.

    Example:
    ```python
    axes = Axes(x_range=(0, 10, 2), y_range=(0, 100, 20), x_length=8, y_length=5)
    point = axes.c2p(5, 50)  # Maps data coordinate (5, 50) to 3D scene point
    ```
    """

    def __init__(
        self,
        x_range: tuple[float, float, float] = (0.0, 10.0, 1.0),
        y_range: tuple[float, float, float] = (0.0, 10.0, 1.0),
        *,
        x_length: float = 8.0,
        y_length: float = 5.0,
        axis_color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        active_theme = get_active_theme()
        resolved_color = axis_color if axis_color is not None else active_theme.colors.border
        cfg = config or ComponentConfig(
            color=resolved_color,
            stroke_color=resolved_color,
            stroke_width=active_theme.strokes.regular,
        )

        self.x_range: tuple[float, float, float] = (
            float(x_range[0]),
            float(x_range[1]),
            float(x_range[2]),
        )
        self.y_range: tuple[float, float, float] = (
            float(y_range[0]),
            float(y_range[1]),
            float(y_range[2]),
        )
        self.x_length: float = float(x_length)
        self.y_length: float = float(y_length)

        super().__init__(config=cfg, **kwargs)

    # -------------------------------------------------------------------------
    # Pure Mathematical Coordinate Mapping (Dual-Correctness Principle)
    # -------------------------------------------------------------------------
    def c2p(self, x: float, y: float, z: float = 0.0) -> np.ndarray:
        """Convert data-space coordinates (x, y) to scene-space 3D vector [X, Y, Z]."""
        x_min, x_max, _ = self.x_range
        y_min, y_max, _ = self.y_range

        x_span = x_max - x_min if abs(x_max - x_min) > 1e-6 else 1.0
        y_span = y_max - y_min if abs(y_max - y_min) > 1e-6 else 1.0

        # Normalized coordinates [0, 1] relative to min
        norm_x = (x - x_min) / x_span
        norm_y = (y - y_min) / y_span

        # Scene coordinates relative to axes center
        scene_center = self.center
        left_x = scene_center[0] - (self.x_length / 2.0)
        bottom_y = scene_center[1] - (self.y_length / 2.0)

        scene_x = left_x + (norm_x * self.x_length)
        scene_y = bottom_y + (norm_y * self.y_length)
        scene_z = scene_center[2] + z

        return np.array([scene_x, scene_y, scene_z], dtype=float)

    def p2c(self, point: Sequence[float] | np.ndarray) -> tuple[float, float]:
        """Convert scene-space 3D coordinate vector to data-space (x, y)."""
        pt = np.asarray(point, dtype=float)
        x_min, x_max, _ = self.x_range
        y_min, y_max, _ = self.y_range

        x_span = x_max - x_min
        y_span = y_max - y_min

        scene_center = self.center
        left_x = scene_center[0] - (self.x_length / 2.0)
        bottom_y = scene_center[1] - (self.y_length / 2.0)

        norm_x = (pt[0] - left_x) / self.x_length
        norm_y = (pt[1] - bottom_y) / self.y_length

        data_x = x_min + (norm_x * x_span)
        data_y = y_min + (norm_y * y_span)

        return float(data_x), float(data_y)

    def _build_mobject(self) -> manim.Mobject:
        """Construct underlying Manim Axes mobject."""
        active_theme = get_active_theme()
        color = self.config.stroke_color or active_theme.colors.border

        mob = manim.Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=self.x_length,
            y_length=self.y_length,
            axis_config={
                "color": color,
                "stroke_width": self.config.stroke_width,
                "include_ticks": True,
            },
        )
        return mob

    def animate_create(self, run_time: float | None = None) -> Animation:
        """Animate drawing the axes."""
        active_theme = get_active_theme()
        duration = run_time if run_time is not None else active_theme.timing.normal
        return Animation(
            component=self,
            manim_animation=manim.Create(self.manim_object),
            run_time=duration,
            name="create_axes",
        )


__all__ = [
    "Axes",
]
