# Automatic Layout System

Animora decouples geometric layout computation from visual components. Layout engines in `animora.layout` are pure algorithmic solvers operating on synthetic bounding boxes (`LayoutItem`), producing positioned output coordinates (`LayoutResult`).

---

## 1. Available Layout Engines

| Layout | Purpose | Key Parameters |
|---|---|---|
| **`HorizontalLayout`** | Left-to-right alignment | `spacing`, `alignment` (top/center/bottom) |
| **`VerticalLayout`** | Top-to-bottom stacking | `spacing`, `alignment` (left/center/right) |
| **`GridLayout`** | 2D matrix rows/columns | `columns`, `col_spacing`, `row_spacing` |
| **`CircularLayout`** | Radial angular distribution | `radius`, `start_angle`, `end_angle` |
| **`TreeLayout`** | Hierarchical tree distribution | `root_id`, `tree_hierarchy`, `level_height` |
| **`GraphLayout`** | Force-directed network embedding | `nodes`, `edges`, `algorithm` (spring/circular) |
| **`FlowLayout`** | Sequential step chain | `step_spacing`, `direction`, `max_per_line` |

---

## 2. Using `Group.arrange()`

Any `Group` of components can be automatically arranged via any layout engine:

```python
from animora.components import Group, Shape
from animora.layout import GridLayout, CircularLayout

items = [Shape.circle(radius=0.4) for _ in range(8)]
group = Group(*items)

# 1. Arrange in a 2x4 Grid
group.arrange(GridLayout(columns=4, col_spacing=0.5, row_spacing=0.5))

# 2. Re-arrange into a Circle
group.arrange(CircularLayout(radius=2.0))
```
