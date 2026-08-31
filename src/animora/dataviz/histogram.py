"""Histogram data visualization component with NumPy-verified binning."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.shape import Shape
from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.config import ComponentConfig
from animora.dataviz.axes import Axes
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class Histogram(Component):
    """An animated histogram component for visualizing numerical frequency distributions.

    Separates statistical binning (computational correctness matching numpy.histogram)
    from visual animation rendering.

    Example:
    ```python
    data = [1.2, 1.5, 2.1, 2.8, 2.9, 3.1, 3.4, 4.2, 4.8, 5.0]
    hist = Histogram(data=data, bins=5)
    scene.play(hist.animate_grow())
    ```
    """

    def __init__(
        self,
        data: Sequence[float] | np.ndarray,
        bins: int | Sequence[float] = 10,
        *,
        axes: Axes | None = None,
        bar_color: str | None = None,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._raw_data = np.asarray(data, dtype=float)
        self._bins_spec = bins
        self._bar_color = bar_color

        # 1. Compute statistical binning
        self._counts, self._bin_edges = self.compute_histogram(self._raw_data, self._bins_spec)

        # 2. Setup Axes
        if axes is None:
            x_min = float(self._bin_edges[0])
            x_max = float(self._bin_edges[-1])
            max_count = float(np.max(self._counts)) if len(self._counts) > 0 else 10.0
            y_max = float(np.ceil(max_count * 1.2)) if max_count > 0 else 10.0

            x_step = (x_max - x_min) / max(1, len(self._counts))
            y_step = max(1.0, y_max / 5.0)

            self._axes = Axes(
                x_range=(x_min, x_max, x_step),
                y_range=(0.0, y_max, y_step),
                x_length=8.0,
                y_length=5.0,
            )
        else:
            self._axes = axes

        self._bars: list[Shape] = []
        super().__init__(config=config, **kwargs)

    @property
    def counts(self) -> np.ndarray:
        """Computed frequency counts per bin."""
        return self._counts

    @property
    def bin_edges(self) -> np.ndarray:
        """Computed bin edge boundaries."""
        return self._bin_edges

    @property
    def axes(self) -> Axes:
        """The coordinate Axes used for mapping."""
        return self._axes

    # -------------------------------------------------------------------------
    # Pure Data Transformation (Verified against NumPy)
    # -------------------------------------------------------------------------
    @staticmethod
    def compute_histogram(
        data: np.ndarray | Sequence[float],
        bins: int | Sequence[float] = 10,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute frequency counts and bin edges matching numpy.histogram."""
        counts, edges = np.histogram(data, bins=bins)
        return counts, edges

    def _build_mobject(self) -> manim.Mobject:
        """Construct the Axes and adjacent histogram bars."""
        active_theme = get_active_theme()
        bar_fill = self._bar_color or active_theme.colors.secondary

        self._bars = []
        all_mobjects: list[manim.Mobject] = [self._axes.manim_object]

        for i in range(len(self._counts)):
            x_left = float(self._bin_edges[i])
            x_right = float(self._bin_edges[i + 1])
            count = float(self._counts[i])

            p_bl = self._axes.c2p(x_left, 0.0)
            p_tr = self._axes.c2p(x_right, count)

            w = max(1e-3, float(abs(p_tr[0] - p_bl[0])))
            h = max(1e-3, float(abs(p_tr[1] - p_bl[1])))
            cx = (p_bl[0] + p_tr[0]) / 2.0
            cy = (p_bl[1] + p_tr[1]) / 2.0

            bar = Shape.rectangle(
                width=w,
                height=h,
                fill_color=bar_fill,
                fill_opacity=0.85,
                stroke_color=active_theme.colors.background,
                stroke_width=active_theme.strokes.thin,
            ).move_to([cx, cy, 0.0])

            self._bars.append(bar)
            all_mobjects.append(bar.manim_object)

        return manim.VGroup(*all_mobjects)

    def animate_grow(self, run_time: float | None = None) -> Animation:
        """Animate histogram bars growing from baseline."""
        active_theme = get_active_theme()
        duration = run_time or active_theme.timing.normal

        bar_mobjects = [bar.manim_object for bar in self._bars]
        return Animation(
            component=self,
            manim_animation=manim.AnimationGroup(
                *[manim.GrowFromPoint(bm, bm.get_bottom()) for bm in bar_mobjects],
                run_time=duration,
            ),
            run_time=duration,
            name="grow_histogram",
        )


__all__ = [
    "Histogram",
]
