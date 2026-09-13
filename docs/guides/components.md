# Visual Component Primitives

Animora's visual primitives provide high-level, declarative building blocks for educational animations. Every component wraps underlying Manim mobjects, implements geometric bounding box positioning, provides semantic animations, and exposes the `.manim_object` escape hatch.

---

## 1. Components Catalog

### `Text`
High-level typography and label component with multi-line support and text transitions.
```python
from animora.components import Text

title = Text("Binary Search", font_size=36, color="#38BDF8")
scene.play(title.animate_transform_text("Linear Search"))
```

### `Shape`
Geometric shapes covering circles, rectangles, rounded rectangles, and arbitrary polygons.
```python
from animora.components import Shape

circle = Shape.circle(radius=0.5, fill_color="#38BDF8")
rect = Shape.rounded_rectangle(width=2.0, height=1.0, corner_radius=0.1)
scene.play(circle.animate_highlight(color="#F59E0B"))
```

### `Connector` & `Arrow`
Straight or curved connecting lines and directional arrows between components or coordinate points.
```python
from animora.components import Arrow, Shape

node_a = Shape.circle().move_to([-2, 0, 0])
node_b = Shape.circle().move_to([2, 0, 0])
edge = Arrow(start=node_a, end=node_b, stroke_color="#94A3B8")
```

### `Group`
Hierarchical composite container of child components supporting multi-element positioning, bounding boxes, and layout arrangement (`Group.arrange(layout)`).
```python
from animora.components import Group

grp = Group(node_a, node_b)
grp.move_to([0, 1, 0])
```

### `Panel`
Framed background container card wrapping child components with optional header title.
```python
from animora.components import Panel, Text

code_text = Text("x = 42", font_size=24)
panel = Panel(code_text, title="Code Snippet")
```

### `Annotation`
Educational callouts, pointers, and badges attached to components or sub-elements.

Every component supports `.annotate(target=None, text=..., direction=..., buff=..., arrow=True, box=False)` returning an `Animation` directly playable in `scene.play()`.

#### Example 1: Annotating an Array Element During a Swap
```python
import manim
from animora.core import Scene
from animora.datastructures import Array
from animora.theme import ModernDark, use_theme


class ArrayAnnotationScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            arr = Array([45, 12, 89, 33])
            self.play(arr.animate_create())

            # Annotate the pivot element at index 2
            self.play(arr.annotate(2, text="Pivot: 89", direction=manim.UP, box=True))

            # Perform swap and highlight
            self.play(arr.animate_swap(0, 2))
```

#### Example 2: Annotating a Binary Search Tree (BST) Node
```python
import manim
from animora.core import Scene
from animora.datastructures import BST
from animora.theme import ModernDark, use_theme


class BSTAnnotationScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            bst = BST([50, 25, 75, 10, 30])
            self.play(bst.animate_create())

            # Annotate the root node with a directional arrow
            self.play(bst.annotate(50, text="Root Node", direction=manim.UP, arrow=True))

            # Annotate leaf during traversal
            self.play(bst.annotate(10, text="Minimum Leaf", direction=manim.DOWN, box=True))
```

---

## 2. Escape Hatch Pattern

Every Animora component exposes its underlying Manim mobject via `@property def manim_object`:

```python
# Access native Manim object whenever low-level manipulation is needed
native_mobj = circle.manim_object
```
