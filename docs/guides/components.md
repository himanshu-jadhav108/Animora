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

---

## 2. Escape Hatch Pattern

Every Animora component exposes its underlying Manim mobject via `@property def manim_object`:

```python
# Access native Manim object whenever low-level manipulation is needed
native_mobj = circle.manim_object
```
