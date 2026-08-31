"""Base Component class for Animora visual elements."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.config import BoundingBox, ComponentConfig

if TYPE_CHECKING:
    from typing_extensions import Self


class Component(ABC):
    """Abstract base class for all visual components in Animora.

    Encapsulates visual state, geometric measurement, spatial manipulation,
    and animation generation while exposing a first-class escape hatch
    (.manim_object) to the underlying Manim vector entity.
    """

    def __init__(
        self,
        *args: Any,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self._config: ComponentConfig = config or ComponentConfig()
        self._mobject: manim.Mobject | None = None
        self._children: list[Component] = []
        self._cached_bbox: BoundingBox | None = None

    # -------------------------------------------------------------------------
    # The Manim Escape Hatch
    # -------------------------------------------------------------------------
    @property
    def manim_object(self) -> manim.Mobject:
        """First-class escape hatch exposing the raw Manim Mobject/VMobject."""
        if self._mobject is None:
            self._mobject = self._build_mobject()
        return self._mobject

    @abstractmethod
    def _build_mobject(self) -> manim.Mobject:
        """Construct and return the initial Manim Mobject/VMobject representation."""
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Configuration & Styling
    # -------------------------------------------------------------------------
    @property
    def config(self) -> ComponentConfig:
        """Visual configuration parameters for this component."""
        return self._config

    # -------------------------------------------------------------------------
    # Geometric Dimensions & Spatial Bounds
    # -------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """Width of the component along the X axis."""
        return float(self.manim_object.width)

    @property
    def height(self) -> float:
        """Height of the component along the Y axis."""
        return float(self.manim_object.height)

    @property
    def depth(self) -> float:
        """Depth of the component along the Z axis."""
        return float(self.manim_object.depth)

    @property
    def center(self) -> np.ndarray:
        """3D center coordinate array [x, y, z] of the component."""
        return np.array(self.manim_object.get_center())

    @property
    def bounding_box(self) -> BoundingBox:
        """Axis-aligned 3D bounding box for layout calculations."""
        if self._cached_bbox is None:
            mob = self.manim_object
            min_pt = mob.get_corner(manim.DL)
            max_pt = mob.get_corner(manim.UR)
            self._cached_bbox = BoundingBox(
                min_point=(float(min_pt[0]), float(min_pt[1]), float(min_pt[2])),
                max_point=(float(max_pt[0]), float(max_pt[1]), float(max_pt[2])),
            )
        return self._cached_bbox

    def _invalidate_bbox_cache(self) -> None:
        """Invalidate cached bounding box calculations."""
        self._cached_bbox = None

    # -------------------------------------------------------------------------
    # Spatial Positioning & Alignment (Fluent API)
    # -------------------------------------------------------------------------
    def move_to(self, target: np.ndarray | Sequence[float] | Component | manim.Mobject) -> Self:
        """Move the component's center to the specified coordinate or target center."""
        self._invalidate_bbox_cache()
        if isinstance(target, Component):
            self.manim_object.move_to(target.manim_object)
        else:
            self.manim_object.move_to(target)
        return self

    def shift(self, vector: np.ndarray | Sequence[float]) -> Self:
        """Shift the component by a relative offset vector."""
        self._invalidate_bbox_cache()
        self.manim_object.shift(vector)
        return self

    def next_to(
        self,
        target: Component | manim.Mobject,
        direction: np.ndarray | Sequence[float] = manim.RIGHT,
        buff: float = 0.5,
    ) -> Self:
        """Position this component adjacent to target along a given direction vector."""
        target_mob = target.manim_object if isinstance(target, Component) else target
        self.manim_object.next_to(target_mob, direction=direction, buff=buff)
        return self

    def align_to(
        self,
        target: Component | manim.Mobject,
        direction: np.ndarray | Sequence[float] = manim.UP,
    ) -> Self:
        """Align this component's edge to target along the specified direction vector."""
        target_mob = target.manim_object if isinstance(target, Component) else target
        self.manim_object.align_to(target_mob, direction=direction)
        return self

    def scale(self, scale_factor: float) -> Self:
        """Scale the component by a multiplicative scalar factor."""
        self.manim_object.scale(scale_factor)
        return self

    # -------------------------------------------------------------------------
    # Semantic Animation Generators
    # -------------------------------------------------------------------------
    def animate_create(self, run_time: float = 1.0) -> Animation:
        """Produce a creation/draw animation."""
        return Animation(
            component=self,
            manim_animation=manim.Create(self.manim_object),
            run_time=run_time,
            name="create",
        )

    def animate_fade_in(self, run_time: float = 1.0) -> Animation:
        """Produce a fade-in opacity animation."""
        return Animation(
            component=self,
            manim_animation=manim.FadeIn(self.manim_object),
            run_time=run_time,
            name="fade_in",
        )

    def animate_fade_out(self, run_time: float = 1.0) -> Animation:
        """Produce a fade-out opacity animation."""
        return Animation(
            component=self,
            manim_animation=manim.FadeOut(self.manim_object),
            run_time=run_time,
            name="fade_out",
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} width={self.width:.2f} height={self.height:.2f}>"


__all__ = [
    "Component",
]
