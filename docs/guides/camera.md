# Camera Control & Viewport Framing

Animora provides a camera convenience wrapper (`animora.core.Camera`) built on top of Manim's `MovingCameraScene`. It offers semantic viewport manipulation with automated bounding-box calculation, smooth multi-object framing, target tracking, and reset transitions.

---

## 1. Quick Start

To enable dynamic camera movements in your animations, subclass `MovingCameraScene` and instantiate `Camera(self)`:

```python
from animora.core import MovingCameraScene, Camera
from animora.datastructures import Array
from animora.theme import ModernDark, use_theme


class CameraDemoScene(MovingCameraScene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            arr = Array([10, 20, 30, 40, 50, 60, 70, 80])
            self.play(arr.animate_create())

            cam = Camera(self)

            # 1. Focus onto a specific subarray or element
            cam.focus(arr, scale=0.7, run_time=1.5)

            # 2. Reset back to the default wide viewport
            cam.reset(run_time=1.2)
```

---

## 2. Core Camera Operations

### `camera.focus(target, scale=1.0, run_time=1.0, rate_func=...)`
Smoothly animates the camera frame to center on `target` (either an Animora `Component` or a Manim `Mobject`).
- `target`: The element to center the viewport on.
- `scale`: Zoom multiplier. Values $< 1.0$ zoom in closer; values $> 1.0$ zoom out.

```python
# Zoom in tightly on the 4th array element
target_box = arr.get_cell(3)
cam.focus(target_box, scale=0.5, run_time=1.0)
```

---

### `camera.fit(targets, padding=0.5, run_time=1.0, rate_func=...)`
Dynamically computes the joint bounding box enclosing a list of objects and fits the viewport around them with clean padding.

```python
# Frame both an Array and a BarChart side-by-side
cam.fit([arr, chart], padding=0.8, run_time=1.5)
```

---

### `camera.follow(target, auto_update=True)` & `camera.unfollow()`
Locks the camera's center position to follow a moving target.
- `auto_update=True`: Attaches an updater callback that pans the camera in real time as the target moves across the screen.
- Call `cam.unfollow()` to detach the updater when target tracking is complete.

```python
# Follow a node moving through a graph traversal
cam.follow(active_node)
self.play(active_node.animate.shift([3, 1, 0]))
cam.unfollow()
```

---

### `camera.reset(run_time=1.0, rate_func=...)`
Restores the camera frame to origin `(0, 0, 0)` with the default screen dimensions (`14.22` width $\times$ `8.0` height).

```python
cam.reset(run_time=1.0)
```

---

## 3. Error Handling and Degradation

`Camera` requires access to a camera frame with `.move_to()` and `.set_width()`, which is provided natively by `MovingCameraScene`.

If `Camera` is initialized with a standard `Scene` that does not support camera movement, it raises a clear, actionable error:

```python
from animora.core import Scene, Camera


class StaticScene(Scene):
    def construct(self) -> None:
        cam = Camera(self)  # Raises TypeError with helpful migration instructions
```

> **Error Message:**  
> `TypeError: Camera requires a MovingCameraScene (or a Scene with a movable camera frame). Got: StaticScene.`
