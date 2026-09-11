"""Camera convenience wrapper and MovingCameraScene for Animora.

Provides declarative camera operations (`focus`, `follow`, `fit`, `reset`)
with graceful error handling when used in non-moving camera scenes.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.core.animation import Animation
from animora.core.component import Component
from animora.core.scene import Scene

if TYPE_CHECKING:
    pass


class Camera:
    """Convenience controller for camera movement, zooming, and tracking.

    Wraps a scene's camera frame to provide declarative panning, zooming (`focus`),
    multi-object framing (`fit`), and continuous tracking (`follow`).

    Example:
    ```python
    class MyScene(MovingCameraScene):
        def construct(self) -> None:
            node = Shape.circle()
            self.add(node)
            self.play(self.cam.focus(node, zoom=2.0))
    ```
    """

    def __init__(self, scene: manim.Scene) -> None:
        self._scene = scene
        self._target_follower: Component | manim.Mobject | None = None
        self._follow_updater: Any = None

    @property
    def frame(self) -> manim.Mobject:
        """Access the underlying movable camera frame, raising if unsupported."""
        camera = getattr(self._scene, "camera", None)
        frame = getattr(camera, "frame", None)
        if frame is None:
            raise RuntimeError(
                "Camera operations (focus, fit, follow, reset) require a scene with a "
                "movable camera frame. Please inherit from animora.core.camera.MovingCameraScene "
                "or manim.MovingCameraScene instead of standard Scene."
            )
        return frame

    def focus(
        self,
        target: Component | manim.Mobject | Sequence[float] | np.ndarray,
        zoom: float = 1.0,
        run_time: float = 1.0,
    ) -> Animation:
        """Animate the camera to center on a target with specified magnification.

        Args:
            target: Component, Mobject, or 3D coordinate vector [x, y, z].
            zoom: Magnification factor (1.0 = normal, 2.0 = 2x zoom-in, 0.5 = zoom-out).
            run_time: Duration of camera pan and zoom in seconds.

        Returns:
            Animora Animation to pass to scene.play().
        """
        center = self._extract_center(target)
        target_width = float(manim.config.frame_width) / max(float(zoom), 0.01)
        anim_builder = self.frame.animate(run_time=run_time).move_to(center).set(width=target_width)
        return Animation(
            component=None,
            manim_animation=anim_builder.build(),
            run_time=run_time,
            name=f"camera_focus(zoom={zoom})",
        )

    def fit(
        self,
        *targets: Component | manim.Mobject,
        padding: float = 0.5,
        run_time: float = 1.0,
    ) -> Animation:
        """Animate the camera frame to encompass all specified targets with padding.

        Args:
            *targets: One or more components or mobjects to fit into view.
            padding: Margin in scene units added around the bounding box.
            run_time: Duration of the framing animation in seconds.

        Returns:
            Animora Animation to pass to scene.play().
        """
        if not targets:
            return self.reset(run_time=run_time)

        mobjects: list[manim.Mobject] = [
            t.manim_object if isinstance(t, Component) else t for t in targets
        ]
        group = manim.Group(*mobjects)
        target_center = group.get_center()

        # Compute bounding dimensions with padding
        target_width = group.width + 2.0 * float(padding)
        target_height = group.height + 2.0 * float(padding)

        # Respect standard camera aspect ratio
        aspect = float(manim.config.frame_width) / float(manim.config.frame_height)
        if target_width / max(target_height, 0.01) < aspect:
            target_width = target_height * aspect

        anim_builder = (
            self.frame.animate(run_time=run_time).move_to(target_center).set(width=target_width)
        )
        return Animation(
            component=None,
            manim_animation=anim_builder.build(),
            run_time=run_time,
            name="camera_fit",
        )

    def follow(self, target: Component | manim.Mobject) -> None:
        """Continuously keep the camera centered on a moving target."""
        self.unfollow()
        self._target_follower = target

        def _follow(mob: manim.Mobject) -> None:
            if self._target_follower is not None:
                center = self._extract_center(self._target_follower)
                mob.move_to(center)

        self._follow_updater = _follow
        self.frame.add_updater(self._follow_updater)

    def unfollow(self) -> None:
        """Stop tracking the target currently followed by the camera."""
        if self._follow_updater is not None:
            self.frame.remove_updater(self._follow_updater)
            self._follow_updater = None
        self._target_follower = None

    def reset(self, run_time: float = 1.0) -> Animation:
        """Animate the camera back to default center origin and default framing."""
        self.unfollow()
        anim_builder = (
            self.frame.animate(run_time=run_time)
            .move_to([0.0, 0.0, 0.0])
            .set(width=manim.config.frame_width)
        )
        return Animation(
            component=None,
            manim_animation=anim_builder.build(),
            run_time=run_time,
            name="camera_reset",
        )

    @staticmethod
    def _extract_center(
        target: Component | manim.Mobject | Sequence[float] | np.ndarray,
    ) -> np.ndarray:
        """Extract a 3D center vector from Component, Mobject, or coordinate array."""
        if isinstance(target, Component):
            return np.array(target.center, dtype=np.float64)
        if isinstance(target, manim.Mobject):
            return np.array(target.get_center(), dtype=np.float64)
        arr = np.array(target, dtype=np.float64)
        if arr.shape == (2,):
            return np.array([arr[0], arr[1], 0.0], dtype=np.float64)
        if arr.shape == (3,):
            return arr
        raise ValueError(f"Target coordinate must have 2 or 3 dimensions, got shape {arr.shape}")


class MovingCameraScene(Scene, manim.MovingCameraScene):  # type: ignore[misc]
    """Animora Scene with moving camera capabilities and camera helper."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._cam: Camera | None = None

    @property
    def cam(self) -> Camera:
        """Convenient access to the Animora Camera controller."""
        if self._cam is None:
            self._cam = Camera(self)
        return self._cam

    @property
    def camera_controller(self) -> Camera:
        """Alias for self.cam."""
        return self.cam


__all__ = [
    "Camera",
    "MovingCameraScene",
]
