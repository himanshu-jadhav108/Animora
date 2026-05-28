# Animora Layout System (Phase 4 Reference)

## 1. Overview & Architecture

Animora features a pure geometric layout engine housed under `animora.layout`. Following the foundational architectural decision from Phase 0, **layouts are pure coordinate solvers decoupled from Manim rendering and `Component` internals**.

```mermaid
graph LR
    subgraph Components
        Group["Group(node1, node2, ...)"]
    end
    
    subgraph Layout Engine
        Item["LayoutItem(id, w, h)"]
        Solver["LayoutSolver.solve(items)"]
        Result["LayoutResult(positions)"]
    end
    
    Group -->|Translates children to| Item
    Item --> Solver
    Solver --> Result
    Result -->|Applies .move_to() on children| Group
```

---

## 2. Layout Algorithms

| Layout Class | Description | Key Parameters |
|---|---|---|
| **`HorizontalLayout`** | Arranges items in a horizontal line from left to right. | `spacing`, `alignment` ("top", "center", "bottom"), `center_origin` |
| **`VerticalLayout`** | Arranges items in a vertical column from top to bottom. | `spacing`, `alignment` ("left", "center", "right"), `center_origin` |
| **`GridLayout`** | Arranges items in a uniform 2D matrix. | `rows`, `columns`, `col_spacing`, `row_spacing` |
| **`CircularLayout`** | Distributes items radially around a circle or arc. | `radius`, `start_angle`, `end_angle`, `clockwise`, `center` |
| **`TreeLayout`** | Hierarchical parent-over-children placement with arbitrary branching. | `edges`, `root_id`, `node_spacing`, `level_spacing`, `direction` |
| **`GraphLayout`** | Force-directed (spring), circular, and spectral network layouts. | `edges`, `algorithm`, `scale`, `iterations`, `seed` |
| **`FlowLayout`** | Sequential step-based chain with line wrapping. | `direction`, `spacing`, `line_spacing`, `wrap_after` |

---

## 3. Integration with `Group.arrange()`

Any composite `Group` of components can be automatically organized with any layout solver:

```python
from animora.core import Scene
from animora.components import Group, Shape, Text
from animora.layout import GridLayout, TreeLayout, CircularLayout

class LayoutDemoScene(Scene):
    def construct(self):
        # 1. Grid of nodes
        nodes = [Shape.circle(radius=0.4, fill_color="#38BDF8") for _ in range(6)]
        grid = Group(*nodes)
        grid.arrange(GridLayout(columns=3, col_spacing=0.5, row_spacing=0.5))

        # 2. Hierarchical Tree
        tree_nodes = [Shape.circle(radius=0.3) for _ in range(5)]
        tree = Group(*tree_nodes)
        tree.arrange(TreeLayout(
            edges=[("0", "1"), ("0", "2"), ("1", "3"), ("1", "4")],
            root_id="0",
            level_spacing=1.5,
            node_spacing=1.0,
        ))

        self.play(grid.animate_fade_in())
```
