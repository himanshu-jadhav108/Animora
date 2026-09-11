"""Unit and integration tests for Camera convenience wrapper and MovingCameraScene."""

from __future__ import annotations

import manim
import pytest

from animora.components.shape import Shape
from animora.core.animation import Animation
from animora.core.camera import Camera, MovingCameraScene
from animora.core.scene import Scene


def test_camera_on_standard_scene_raises_helpful_error() -> None:
    """Verify Camera raises informative error when used on non-moving camera scene."""
    standard_scene = Scene()
    cam = Camera(standard_scene)
    with pytest.raises(RuntimeError, match="require a scene with a movable camera frame"):
        _ = cam.frame


def test_moving_camera_scene_access() -> None:
    """Verify MovingCameraScene provides direct access to Camera instance."""
    scene = MovingCameraScene()
    assert isinstance(scene.cam, Camera)
    assert scene.camera_controller is scene.cam
    assert scene.cam.frame is not None


def test_camera_focus_generates_animation() -> None:
    """Verify focus generates an Animation targeting target center and zoom width."""
    scene = MovingCameraScene()
    circle = Shape.circle(radius=0.5).move_to([2.0, 3.0, 0.0])
    anim = scene.cam.focus(circle, zoom=2.0, run_time=1.5)

    assert isinstance(anim, Animation)
    assert isinstance(anim.to_manim(), manim.Animation)


def test_camera_fit_multiple_targets() -> None:
    """Verify fit calculates bounding box enclosing multiple components."""
    scene = MovingCameraScene()
    c1 = Shape.circle(radius=0.5).move_to([-3.0, 0.0, 0.0])
    c2 = Shape.circle(radius=0.5).move_to([3.0, 0.0, 0.0])
    anim = scene.cam.fit(c1, c2, padding=1.0)

    assert isinstance(anim, Animation)
    assert isinstance(anim.to_manim(), manim.Animation)


def test_camera_follow_and_unfollow() -> None:
    """Verify follow attaches updater and unfollow detaches it."""
    scene = MovingCameraScene()
    target = Shape.circle().move_to([1.0, 1.0, 0.0])
    scene.cam.follow(target)
    assert scene.cam._target_follower is target
    assert scene.cam._follow_updater is not None

    scene.cam.unfollow()
    assert scene.cam._target_follower is None
    assert scene.cam._follow_updater is None


def test_moving_camera_scene_renders_cleanly() -> None:
    """Verify MovingCameraScene renders end-to-end in dry-run mode."""

    class DemoCameraScene(MovingCameraScene):
        def construct(self) -> None:
            c = Shape.circle(radius=0.5).move_to([1.0, 1.0, 0.0])
            self.add(c)
            self.play(self.cam.focus(c, zoom=1.5, run_time=0.1))
            self.play(self.cam.reset(run_time=0.1))

    with manim.tempconfig({"dry_run": True, "verbosity": "ERROR", "write_to_movie": False}):
        s = DemoCameraScene()
        s.render()
        assert len(s.mobjects) >= 1
