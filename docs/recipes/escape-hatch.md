# Recipe: Using the Manim Escape Hatch

## Goal
Access and manipulate underlying Manim `Mobject`s directly when you need custom Manim shaders, low-level point manipulators, or specialized updater functions.

---

## Solution

Every Animora `Component` provides the `.manim_object` property:

```python
import manim
from animora.core import Scene
from animora.components import Shape

class ManimEscapeHatchScene(Scene):
    def construct(self) -> None:
        circle = Shape.circle(radius=1.0)
        
        # Access native Manim VMobject
        native_mobj = circle.manim_object
        
        # Apply direct Manim methods (e.g. updater or color gradient)
        native_mobj.set_color_by_gradient(manim.BLUE, manim.GREEN)
        
        # Play directly with scene
        self.play(manim.Rotate(native_mobj, angle=manim.PI))
```
