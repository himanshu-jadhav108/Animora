# Animora Architecture — Core Abstractions (Phase 2 Reference)

## 1. Overview & Purpose

Phase 2 introduces the foundational class hierarchy for **Animora**, establishing the core bridge between high-level declarative components and Manim's imperative rendering engine.

```mermaid
classDiagram
    class ComponentConfig {
        +str color
        +str fill_color
        +float fill_opacity
        +str stroke_color
        +float stroke_width
        +float font_size
        +str font_family
        +merge(**overrides) ComponentConfig
    }

    class Component {
        <<abstract>>
        #ComponentConfig _config
        #Mobject _mobject
        +manim_object: Mobject
        +width: float
        +height: float
        +depth: float
        +center: ndarray
        +bounding_box: BoundingBox
        +move_to(target) Self
        +shift(vector) Self
        +next_to(target, direction, buff) Self
        +align_to(target, direction) Self
        +scale(factor) Self
        +animate_create(run_time) Animation
        +animate_fade_in(run_time) Animation
        +animate_fade_out(run_time) Animation
        #_build_mobject()* Mobject
    }

    class Label {
        -str _text_content
        +text: str
        +set_text(new_text) Self
        +animate_transform_text(new_text, run_time) Animation
    }

    class Animation {
        -Component _component
        -manim.Animation _manim_animation
        -float _run_time
        +component: Component
        +run_time: float
        +name: str
        +to_manim() manim.Animation
    }

    class Scene {
        -List~Component~ _registered_components
        +add(*items)
        +remove(*items)
        +play(*animations_or_components, **kwargs)
    }

    Component <|-- Label
    Component --> ComponentConfig
    Component --> Animation
    Scene o-- Component
```

---

## 2. Class Contracts & Specifications

### `animora.core.Component`
The abstract base class for all visual components.
- **Escape Hatch**: `@property def manim_object(self) -> manim.Mobject` lazy-builds and caches the underlying Manim `Mobject`/`VMobject`.
- **Geometry**: `width`, `height`, `depth`, `center`, and `bounding_box` (`BoundingBox`) provide measured coordinates for layout engines.
- **Positioning**: Fluent methods (`move_to`, `shift`, `next_to`, `align_to`, `scale`) mutate the underlying Manim mobject and return `self`.
- **Lifecycle**: Subclasses implement `_build_mobject() -> manim.Mobject`.

### `animora.core.Scene`
Extends `manim.Scene`:
- Tracks registered `Component` instances.
- Automatic unwrapping in `add()` and `remove()`.
- Enhanced `play()` method that accepts `Animation`, `Component` (auto-fades in), or native Manim `Animation`.

### `animora.core.Animation`
Bridges semantic animation intent to Manim:
- Carries target `component`, `run_time`, `rate_func`, and descriptive `name`.
- `.to_manim()` produces the configured `manim.Animation` instance.

### `animora.core.ComponentConfig`
Immutable/mergeable configuration dataclass holding basic visual styling attributes: `color`, `fill_color`, `fill_opacity`, `stroke_color`, `stroke_width`, `font_size`, `font_family`.

### `animora.components.Label`
The reference primitive demonstrating full stack integration:
- Renders text via Manim's `Text`.
- Supports dynamic `set_text()` and `animate_transform_text()`.

---

## 3. The Escape Hatch in Practice

```python
from animora.core import Scene
from animora.components import Label
import manim

class CustomScene(Scene):
    def construct(self):
        # 1. High-level Animora component
        label = Label("Hello, Animora!", color="#38BDF8")
        
        # 2. Add via high-level animation
        self.play(label.animate_fade_in(run_time=1.0))
        
        # 3. Escape hatch to native Manim
        label.manim_object.shift(manim.UP)
        self.play(manim.Wiggle(label.manim_object))
```
