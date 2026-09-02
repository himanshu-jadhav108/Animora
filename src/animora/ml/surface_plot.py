"""Surface and contour plot component for loss landscapes and 2D optimization surfaces."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.ml.base import MLComponent
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class SurfacePlot(MLComponent):
    """Visualizes 2D loss functions and mathematical surfaces as contour maps.

    Reuses `Axes` for spatial coordinate mapping and theme design tokens
    for color gradient resolution.

    Example:
    ```python
    def loss_fn(x: float, y: float) -> float:
        return x**2 + y**2

    surface = SurfacePlot(loss_fn, x_range=(-3, 3, 1), y_range=(-3, 3, 1))
    point_3d = surface.c2p(1.5, 2.0)
    ```
    """

    def __init__(
        self,
        fn: Callable[[float, float], float],
        x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        *,
        x_length: float = 6.0,
        y_length: float = 6.0,
        num_contours: int = 8,
        resolution: int = 25,
        colormap: Sequence[str] | None = None,
        show_axes: bool = True,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.fn = fn
        self.x_range = (float(x_range[0]), float(x_range[1]), float(x_range[2]))
        self.y_range = (float(y_range[0]), float(y_range[1]), float(y_range[2]))
        self.x_length = float(x_length)
        self.y_length = float(y_length)
        self.num_contours = max(2, int(num_contours))
        self.resolution = max(10, int(resolution))
        self.show_axes = show_axes

        active_theme = get_active_theme()
        default_cmap = [
            active_theme.colors.primary,
            active_theme.colors.secondary,
            active_theme.colors.accent,
        ]
        self.colormap = list(colormap) if colormap is not None else default_cmap

        self.axes = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=self.x_length,
            y_length=self.y_length,
        )

        super().__init__(config=config, **kwargs)

    def c2p(self, x: float, y: float, z: float = 0.0) -> np.ndarray:
        """Convert data-space coordinates (x, y) to scene-space 3D vector."""
        return self.axes.c2p(x, y, z)

    def p2c(self, point: Sequence[float] | np.ndarray) -> tuple[float, float]:
        """Convert scene-space vector to data-space coordinates (x, y)."""
        return self.axes.p2c(point)

    def evaluate_grid(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Evaluate mathematical function on a uniform 2D grid."""
        xs = np.linspace(self.x_range[0], self.x_range[1], self.resolution)
        ys = np.linspace(self.y_range[0], self.y_range[1], self.resolution)
        X, Y = np.meshgrid(xs, ys)
        Z = np.zeros_like(X, dtype=float)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = float(self.fn(float(X[i, j]), float(Y[i, j])))
        return X, Y, Z

    def _build_mobject(self) -> manim.Mobject:
        """Construct Manim composite mobject representing the surface contours and axes."""
        group = manim.VGroup()

        if self.show_axes:
            group.add(self.axes.manim_object)

        X, Y, Z = self.evaluate_grid()
        z_min = float(np.min(Z))
        z_max = float(np.max(Z))
        z_span = z_max - z_min if abs(z_max - z_min) > 1e-6 else 1.0

        levels = np.linspace(z_min + (0.05 * z_span), z_max - (0.05 * z_span), self.num_contours)

        contours_group = manim.VGroup()

        # Generate contour segments for each level using a cell-marching approximation
        for lvl_idx, level in enumerate(levels):
            t = lvl_idx / max(1, self.num_contours - 1)
            # Pick color from colormap
            color_idx = min(int(t * (len(self.colormap) - 1)), len(self.colormap) - 1)
            c = self.colormap[color_idx]

            contour_subgroup = manim.VGroup()

            for i in range(self.resolution - 1):
                for j in range(self.resolution - 1):
                    # 4 corners of cell
                    pts = [
                        (X[i, j], Y[i, j], Z[i, j]),
                        (X[i, j + 1], Y[i, j + 1], Z[i, j + 1]),
                        (X[i + 1, j + 1], Y[i + 1, j + 1], Z[i + 1, j + 1]),
                        (X[i + 1, j], Y[i + 1, j], Z[i + 1, j]),
                    ]
                    z_vals = [p[2] for p in pts]
                    if min(z_vals) <= level <= max(z_vals):
                        # Approximate mid-point segment for iso-level crossing
                        x_mid = 0.5 * (X[i, j] + X[i + 1, j + 1])
                        y_mid = 0.5 * (Y[i, j] + Y[i + 1, j + 1])
                        p1 = self.c2p(x_mid - 0.04 * (self.x_range[1] - self.x_range[0]), y_mid)
                        p2 = self.c2p(x_mid + 0.04 * (self.x_range[1] - self.x_range[0]), y_mid)
                        line = manim.Line(p1, p2, color=c, stroke_width=1.8, stroke_opacity=0.7)
                        contour_subgroup.add(line)

            contours_group.add(contour_subgroup)

        group.add(contours_group)
        return group

    def animate_create(self, run_time: float | None = None) -> Animation:
        """Animate creation of axes and contour lines."""
        active_theme = get_active_theme()
        duration = run_time if run_time is not None else active_theme.timing.normal
        return Animation(
            component=self,
            manim_animation=manim.Create(self.manim_object),
            run_time=duration,
            name="create_surface_plot",
        )


__all__ = [
    "SurfacePlot",
]
