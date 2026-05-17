# Animora Architecture — Public API Philosophy & Conventions

## 1. Ergonomic Principles

Animora's public API is designed around four foundational ergonomic tenets:

1. **Declarative Configuration, Imperative Action**: Component construction is declarative (declaring data, styles, and options), while animation sequences are expressed through intuitive, imperative semantic method calls (`graph.highlight_path(...)`, `array.swap(...)`).
2. **Predictable Defaults, Deep Customization**: Every component renders with professional typography, balanced padding, and harmonized colors out of the box without requiring manual styling parameters.
3. **No Black Boxes (First-Class Escape Hatch)**: When a user hits the boundary of Animora’s abstractions, they never need to rewrite their scene. Every component exposes its underlying Manim `VMobject` directly.
4. **Seamless Manim Interoperability**: Animora components can be added to any standard Manim `Scene` via `self.add()` or `self.play()` without requiring a proprietary Animora-only runtime.

---

## 2. The Base `Component` Contract

Every visual element in Animora inherits from `animora.core.Component`. Its public interface consists of five standard facets:

```python
class Component:
    """Base class for all Animora visual components.
    
    (Illustrative specification — non-final implementation)
    """

    # 1. Lifecycle & Construction
    def __init__(self, *args, theme: Theme | None = None, **kwargs) -> None: ...

    # 2. Geometric Dimensions & Bounds
    @property
    def width(self) -> float: ...
    @property
    def height(self) -> float: ...
    @property
    def center(self) -> np.ndarray: ...
    @property
    def bounding_box(self) -> BoundingBox: ...

    # 3. Spatial Positioning & Alignment
    def move_to(self, target: np.ndarray | Component) -> Self: ...
    def next_to(self, target: Component, direction: np.ndarray = RIGHT, buff: float = 0.5) -> Self: ...
    def align_to(self, target: Component, direction: np.ndarray = UP) -> Self: ...
    def scale(self, scale_factor: float) -> Self: ...

    # 4. Semantic Animation Generators (Return Manim Animation objects or AnimationGroup)
    def animate_create(self, run_time: float = 1.0) -> Animation: ...
    def animate_fade_out(self, run_time: float = 1.0) -> Animation: ...
    def animate_transform_to(self, new_state: Any, run_time: float = 1.0) -> Animation: ...

    # 5. The Manim Escape Hatch
    @property
    def manim_object(self) -> VMobject | Mobject:
        """Exposes the underlying Manim Mobject/VMobject/VGroup."""
        ...
```

---

## 3. The Escape Hatch: Interoperability with Raw Manim

A critical requirement of Animora is that users are never trapped inside the abstraction layer. If a user needs a specialized Manim animation (such as `ApplyPointwiseFunction`, `Wiggle`, or custom shaders), they access `.manim_object`.

### Illustrative Example: High-Level Animora + Raw Manim Interoperability

```python
# Illustrative snippet — non-final API demonstration
from manim import Scene, UP, DOWN, PI, Wiggle, Rotate, Circle, BLUE
from animora.components.dsa import Array, Graph
from animora.theme import ModernDarkTheme

class HybridAlgorithmScene(Scene):
    def construct(self):
        # 1. High-level declarative Animora component creation
        arr = Array([42, 17, 89, 5, 23], theme=ModernDarkTheme())
        arr.move_to(UP * 2)

        # 2. Add to standard Manim scene via escape hatch
        self.play(arr.animate_create(run_time=1.5))
        
        # 3. Perform semantic Animora operations
        self.play(arr.animate_swap(0, 3, run_time=1.0))
        self.play(arr.animate_highlight(3, color="#10B981"))

        # 4. ESCAPE HATCH: Use raw Manim objects and low-level Manim animations
        raw_mobject = arr.manim_object
        self.play(Wiggle(raw_mobject))
        self.play(raw_mobject.animate.shift(DOWN * 1.5))

        # 5. Interleave with native Manim primitives
        marker = Circle(radius=0.3, color=BLUE).next_to(raw_mobject, DOWN)
        self.play(Rotate(marker, angle=PI), run_time=0.8)
```

---

## 4. Public vs. Internal API Conventions

Animora enforces strict naming and exposure rules across the entire codebase:

### 1. Explicit `__all__` Lists
Every public module and package `__init__.py` must define an explicit `__all__` list. Only symbols listed in `__all__` are considered part of the public, semantically versioned API.

### 2. Underscore Prefixing for Private Members
- All internal helper functions, private attributes, and non-public methods must be prefixed with a single leading underscore (e.g. `_compute_cell_bounds()`, `_cached_mobject`).
- Double-underscore mangling (`__name`) is discouraged unless specifically required to prevent subclass namespace collisions.

### 3. Internal Submodules (`_internal`)
Implementation details shared across modules that are not part of the public API must reside in subpackages prefixed with an underscore (e.g. `animora.core._internal.geometry_utils`). Code outside the `animora` repository must not import from `_internal`.

### 4. Type Annotations
All public functions, methods, and class attributes must have 100% complete type hints (compatible with `mypy --strict`). Type aliases and protocols are exposed under `animora.core.types`.
