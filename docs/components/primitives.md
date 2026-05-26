# Animora Components — Visual Primitives (Phase 3 Reference)

## 1. Overview

Primitives are the foundational graphical building blocks of Animora. All higher-level visual components—including statistical charts in Phase 6 and data structures in Phase 7—are composed from these six primitive components.

| Primitive | Class | Underneath Manim Representation | Primary Purpose |
|---|---|---|---|
| **Text** | `animora.components.Text` | `manim.Text` | Titles, descriptions, equations, code snippets |
| **Shape** | `animora.components.Shape` | `manim.Circle`, `manim.Rectangle`, `manim.Polygon` | Visual nodes, geometric markers, custom cells |
| **Connector** | `animora.components.Connector` | `manim.Line`, `manim.ArcBetweenPoints` | Non-directional links and connection arcs |
| **Arrow** | `animora.components.Arrow` | `manim.Arrow`, `manim.CurvedArrow` | Directional graph edges, pointers, flowcharts |
| **Group** | `animora.components.Group` | `manim.VGroup`, `manim.Group` | Composite containers of multiple components |
| **Panel** | `animora.components.Panel` | `manim.VGroup` (`Shape` background + content) | Framed cards and state display containers |

---

## 2. Design Resolutions & Architecture Decisions

### 1. `Text` vs. `Label`
- **`Text`**: General-purpose typography component supporting multi-line strings, custom font families, line spacing, and text transformations.
- **`Label`**: Introduced in Phase 2 as the initial reference primitive for text badges. `Label` remains available as an alias/convenience text primitive for annotations.

### 2. `Arrow` & `Connector` Relationship
- **`Connector`** represents a general line or arc between two endpoints (either component centers or 3D coordinate tuples).
- **`Arrow`** subclasses and composes `Connector`, adding configurable directional arrowhead tips (`tip_length`, `buff`).

### 3. `Shape` Factory API
- Uses a unified, configurable `Shape` class with ergonomic class factory methods:
  - `Shape.circle(radius=0.5, ...)`
  - `Shape.rectangle(width=2.0, height=1.0, ...)`
  - `Shape.rounded_rectangle(width=2.0, height=1.0, corner_radius=0.2, ...)`
  - `Shape.polygon(vertices=[...], ...)`

---

## 3. Usage Examples

### Composite Diagram Example

```python
from animora.core import Scene
from animora.components import Text, Shape, Arrow, Group, Panel
import manim

class TreeDemoScene(Scene):
    def construct(self):
        # 1. Typography
        title = Text("Binary Tree Demo", font_size=36, color="#38BDF8")
        title.move_to([0, 3, 0])

        # 2. Shapes
        node_a = Shape.circle(radius=0.4, fill_color="#3B82F6").move_to([-1.5, 0, 0])
        node_b = Shape.circle(radius=0.4, fill_color="#10B981").move_to([1.5, 0, 0])

        # 3. Arrow edge
        edge = Arrow(start=node_a, end=node_b, stroke_color="#38BDF8")

        # 4. Padded Panel framing content
        panel = Panel(node_a, node_b, edge, title="Data Structure Frame", padding=0.4)

        # 5. Play animations
        self.play(title.animate_fade_in(run_time=1.0))
        self.play(panel.animate_create(run_time=1.5))
        self.play(edge.animate_highlight(color="#F59E0B", run_time=0.8))
```
