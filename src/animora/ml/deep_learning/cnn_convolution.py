"""CNN 2D convolution operation model, step-by-step sliding window visualizer, and one-call API."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.ml.tensor_grid import TensorGrid
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class CNNConvolutionModel:
    """Computes exact 2D valid cross-correlation/convolution and records sliding steps."""

    def __init__(
        self,
        image: Sequence[Sequence[float]] | np.ndarray,
        kernel: Sequence[Sequence[float]] | np.ndarray,
        *,
        stride: int = 1,
    ) -> None:
        self.image = np.asarray(image, dtype=float)
        self.kernel = np.asarray(kernel, dtype=float)
        if self.image.ndim != 2 or self.kernel.ndim != 2:
            raise ValueError("image and kernel must both be 2D arrays.")

        h_in, w_in = self.image.shape
        k_h, k_w = self.kernel.shape
        if k_h > h_in or k_w > w_in:
            raise ValueError("Kernel dimensions cannot exceed image dimensions.")

        self.stride = max(1, int(stride))
        self.out_h = ((h_in - k_h) // self.stride) + 1
        self.out_w = ((w_in - k_w) // self.stride) + 1

        self.output = np.zeros((self.out_h, self.out_w), dtype=float)
        self.trace = MLTrace()

    def compute(self) -> list[dict[str, Any]]:
        """Compute the full 2D convolution and record each sliding step."""
        self.trace = MLTrace()
        k_h, k_w = self.kernel.shape
        steps_history: list[dict[str, Any]] = []

        for r in range(self.out_h):
            for c in range(self.out_w):
                row_start = r * self.stride
                col_start = c * self.stride
                window = self.image[row_start : row_start + k_h, col_start : col_start + k_w]
                val = float(np.sum(window * self.kernel))
                self.output[r, c] = val

                entry = {
                    "r": r,
                    "c": c,
                    "row_start": row_start,
                    "col_start": col_start,
                    "val": val,
                    "output_snapshot": self.output.copy(),
                }
                steps_history.append(entry)

                self.trace.record(
                    name="conv_step",
                    description=f"Conv step ({r}, {c}): val={val:.2f}",
                    r=r,
                    c=c,
                    val=val,
                )

        return steps_history


class CNNConvolutionVisualizer(MLComponent):
    """Visualizes 2D CNN convolution with input, kernel, and output tensor grids."""

    def __init__(
        self,
        image: Sequence[Sequence[float]] | np.ndarray,
        kernel: Sequence[Sequence[float]] | np.ndarray,
        *,
        stride: int = 1,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.model = CNNConvolutionModel(image, kernel, stride=stride)
        self.steps = self.model.compute()

        # Build tensor grids
        self.input_grid = TensorGrid(self.model.image, cell_size=0.6, show_labels=True)
        self.kernel_grid = TensorGrid(self.model.kernel, cell_size=0.6, show_labels=True)
        self.output_grid = TensorGrid(self.model.output, cell_size=0.6, show_labels=True)

        # Position grids side by side: [Input]  *  [Kernel]  =  [Output]
        self.input_grid.move_to(np.array([-3.6, 0.0, 0.0]))
        self.kernel_grid.move_to(np.array([0.0, 0.0, 0.0]))
        self.output_grid.move_to(np.array([3.6, 0.0, 0.0]))

        super().__init__(config=config, **kwargs)

    def _build_mobject(self) -> manim.Mobject:
        group = manim.VGroup()
        group.add(self.input_grid.manim_object)
        group.add(self.kernel_grid.manim_object)
        group.add(self.output_grid.manim_object)

        # Mathematical operation symbols
        mult_sym = manim.Text("*", font_size=28, color="#94A3B8").move_to(
            np.array([-1.8, 0.0, 0.0])
        )
        eq_sym = manim.Text("=", font_size=28, color="#94A3B8").move_to(np.array([1.8, 0.0, 0.0]))
        group.add(mult_sym, eq_sym)

        return group

    def animate(self) -> list[Animation]:
        """One-call animation generator for CNN convolution sliding window."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Create layout
        base_group = manim.VGroup(
            self.input_grid.manim_object,
            self.kernel_grid.manim_object,
            self.output_grid.manim_object,
        )
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(base_group),
                run_time=0.8,
                name="create_conv_grids",
            )
        )

        # 2. Sliding window bounding box over input grid
        k_h, k_w = self.model.kernel.shape
        cell_size = 0.6
        box_w = k_w * cell_size
        box_h = k_h * cell_size

        window_box = manim.Rectangle(
            width=box_w,
            height=box_h,
            color=active_theme.colors.accent,
            stroke_width=3.0,
        )
        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Create(window_box),
                run_time=0.3,
                name="init_sliding_window",
            )
        )

        # Animate sliding steps
        input_center = np.array([-3.6, 0.0, 0.0])
        h_in, w_in = self.model.image.shape

        for step_entry in self.steps:
            r = step_entry["r"]
            c = step_entry["c"]
            row_start = step_entry["row_start"]
            col_start = step_entry["col_start"]

            # Compute window box center relative to input grid center
            top_left_x = input_center[0] - (w_in * cell_size / 2.0)
            top_left_y = input_center[1] + (h_in * cell_size / 2.0)

            box_cx = top_left_x + (col_start * cell_size) + (box_w / 2.0)
            box_cy = top_left_y - (row_start * cell_size) - (box_h / 2.0)
            target_pos = np.array([box_cx, box_cy, 0.0])

            animations.append(
                Animation(
                    component=self,
                    manim_animation=window_box.animate.move_to(target_pos),
                    run_time=0.2,
                    name=f"slide_to_{r}_{c}",
                )
            )

        return animations


def cnn_convolution(
    image: Sequence[Sequence[float]] | np.ndarray,
    kernel: Sequence[Sequence[float]] | np.ndarray,
    *,
    stride: int = 1,
) -> list[Animation]:
    """One-call functional API to animate 2D CNN convolution sliding window."""
    viz = CNNConvolutionVisualizer(image, kernel, stride=stride)
    return viz.animate()


__all__ = [
    "CNNConvolutionModel",
    "CNNConvolutionVisualizer",
    "cnn_convolution",
]
