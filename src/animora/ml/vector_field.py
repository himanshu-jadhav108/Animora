"""Vector field component for gradients, vector flows, and directional derivatives."""

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
    from animora.ml.surface_plot import SurfacePlot


class VectorField(MLComponent):
    """Visualizes 2D vector fields and gradient vectors across a coordinate space.

    Samples points across a data grid and renders directional arrows,
    reusing `Axes` for spatial mapping and theme tokens for styling.

    Example:
    ```python
    def neg_grad(x: float, y: float) -> tuple[float, float]:
        return -2 * x, -2 * y

    vf = VectorField(neg_grad, x_range=(-3, 3, 1), y_range=(-3, 3, 1), step=0.8)
    ```
    """

    def __init__(
        self,
        vector_fn: Callable[[float, float], tuple[float, float] | Sequence[float] | np.ndarray],
        x_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        y_range: tuple[float, float, float] = (-3.0, 3.0, 1.0),
        *,
        step: float = 1.0,
        vector_scale: float = 0.35,
        max_arrow_length: float = 0.75,
        normalize: bool = False,
        axes: Axes | SurfacePlot | None = None,
        color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.vector_fn = vector_fn
        self.x_range = (float(x_range[0]), float(x_range[1]), float(x_range[2]))
        self.y_range = (float(y_range[0]), float(y_range[1]), float(y_range[2]))
        self.step = max(0.1, float(step))
        self.vector_scale = float(vector_scale)
        self.max_arrow_length = float(max_arrow_length)
        self.normalize = normalize
        self.custom_color = color

        if axes is not None:
            if hasattr(axes, "axes"):
                self.axes: Axes = axes.axes
            else:
                self.axes = axes
        else:
            self.axes = Axes(x_range=self.x_range, y_range=self.y_range)

        super().__init__(config=config, **kwargs)

    def sample_vectors(self) -> list[tuple[float, float, float, float]]:
        """Sample vector evaluations over regular grid points (x, y, u, v)."""
        samples: list[tuple[float, float, float, float]] = []
        xs = np.arange(self.x_range[0], self.x_range[1] + 1e-5, self.step)
        ys = np.arange(self.y_range[0], self.y_range[1] + 1e-5, self.step)

        for x in xs:
            for y in ys:
                vec = self.vector_fn(float(x), float(y))
                u, v = float(vec[0]), float(vec[1])
                samples.append((float(x), float(y), u, v))
        return samples

    def _build_mobject(self) -> manim.Mobject:
        """Construct Manim composite mobject containing the grid of vector arrows."""
        active_theme = get_active_theme()
        color = self.custom_color or active_theme.colors.accent

        group = manim.VGroup()
        samples = self.sample_vectors()

        for x, y, u, v in samples:
            mag = float(np.hypot(u, v))
            if mag < 1e-5:
                continue

            start_p = self.axes.c2p(x, y)

            if self.normalize:
                dir_u, dir_v = u / mag, v / mag
                arrow_len = self.vector_scale
            else:
                arrow_len = min(mag * self.vector_scale, self.max_arrow_length)
                dir_u, dir_v = u / mag, v / mag

            end_p = start_p + np.array([dir_u * arrow_len, dir_v * arrow_len, 0.0])

            arrow = manim.Arrow(
                start=start_p,
                end=end_p,
                buff=0.0,
                color=color,
                stroke_width=1.8,
                max_tip_length_to_length_ratio=0.35,
                max_stroke_width_to_length_ratio=4.0,
            )
            group.add(arrow)

        return group

    def animate_create(self, run_time: float | None = None) -> Animation:
        """Animate creation of vector field arrows."""
        active_theme = get_active_theme()
        duration = run_time if run_time is not None else active_theme.timing.normal
        return Animation(
            component=self,
            manim_animation=manim.Create(self.manim_object),
            run_time=duration,
            name="create_vector_field",
        )


__all__ = [
    "VectorField",
]
