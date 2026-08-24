# Animora

**High-Level Declarative Animation Framework Built on Manim**

Animora democratizes the creation of publication-quality educational, technical, mathematical, and algorithmic animations through a modern declarative component hierarchy, automatic layout solvers, design token themes, stateful data structures, and verifiable algorithm operation tracing.

---

## Key Highlights

- **Visual Component Primitives**: High-level `Text`, `Shape`, `Connector`, `Arrow`, `Group`, and `Panel` primitives with semantic state animations (`animate_highlight`, `animate_transform`, `animate_create`).
- **Decoupled Automatic Layout Solvers**: Pure geometric layout engines including `HorizontalLayout`, `VerticalLayout`, `GridLayout`, `CircularLayout`, `TreeLayout`, `GraphLayout`, and `FlowLayout`.
- **Theme & Design Token Engine**: Built-in production themes (`ModernDark`, `PaperLight`, `Cyberpunk`, `Monokai`) with dynamic context resolution via `use_theme()`.
- **Data Visualization**: Educational chart components with guaranteed mathematical precision: `Axes`, `BarChart`, `LineChart`, `ScatterPlot`, `Histogram`, and `Table`.
- **Computer Science Data Structures**: Stateful structures isolating pure Python data models from animation layers: `Array`, `Stack`, `Queue`, `LinkedList`, `Heap`, `Tree`, `BST`, `Graph`, and `HashTable`.
- **Verifiable Algorithm Animations**: Explicit `OperationTrace` recording for Searching, 5 Sorting algorithms, BFS/DFS, Dijkstra, A*, DP, and Backtracking.
- **Developer CLI**: Fast prototyping with `animora new`, `animora preview`, `animora render`, and `animora doctor`.

---

## Quick Example

```python
from animora.core import Scene
from animora.datastructures import BST
from animora.theme import ModernDark, use_theme

class BSTDemoScene(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            # 1. Initialize BST
            bst = BST([50, 30, 70, 20, 40])
            self.play(bst.animate_create())

            # 2. Insert new value (animates comparison path 50 -> 30 -> 40 before placement)
            self.play(bst.animate_insert(35))

            # 3. Search target
            self.play(bst.animate_search(35))
```

---

## Next Steps

- **[Installation Guide](getting-started/installation.md)**: Set up Animora, Python, Manim, and FFmpeg.
- **[Your First Scene](getting-started/first-scene.md)**: Step-by-step beginner tutorial.
- **[Guides & Concepts](guides/components.md)**: Deep dive into components, layouts, theming, and algorithms.
- **[Example Gallery](examples/gallery.md)**: Explore runnable code examples.
- **[API Reference](reference/api.md)**: Full reference for all public classes and functions.
