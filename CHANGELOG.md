# Changelog

All notable changes to the **Animora** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-08-26

### Added
- **Core Architecture & Abstractions**:
  - `Component` base class encapsulating visual state, geometric bounds, positioning fluent API, and the `.manim_object` escape hatch.
  - `Scene` high-level declarative wrapper around Manim's Scene supporting polymorphic `.play()`.
  - `Animation` polymorphic bridge wrapping Manim animations.
  - `ComponentConfig` and `BoundingBox` geometry contracts.
- **Visual Primitives (`animora.components`)**:
  - `Text`: Typography component with font styling and text transformation animations (`animate_transform_text`).
  - `Shape`: Versatile geometric primitive (`circle`, `rectangle`, `rounded_rectangle`, `polygon`).
  - `Connector` & `Arrow`: Straight/curved connectors and directional arrows.
  - `Group`: Composite multi-element container with `arrange(layout)`.
  - `Panel`: Padded container card with header titles.
  - `Label`: Text label primitive.
- **Decoupled Layout Engines (`animora.layout`)**:
  - `HorizontalLayout`, `VerticalLayout`, `GridLayout`, `CircularLayout`, `TreeLayout`, `GraphLayout` (NetworkX-powered), and `FlowLayout`.
- **Design Tokens & Theme System (`animora.theme`)**:
  - `ColorPalette`, `Typography`, `SpacingScale`, `StrokeScale`, `CornerRadius`, `AnimationTiming`.
  - Built-in Themes: `ModernDark` (default), `PaperLight`, `Cyberpunk`, and `Monokai`.
  - `use_theme()` context manager for block-level theme scoping.
- **Data Visualization (`animora.dataviz`)**:
  - `Axes`: 2D coordinate system with `c2p()` and `p2c()` mapping.
  - `BarChart`: Proportional bar height scaling with `animate_grow()` and `animate_highlight_bar()`.
  - `LineChart`: Progressive path drawing with `animate_draw()`.
  - `ScatterPlot`: 2D point cloud with `animate_plot()`.
  - `Histogram`: Statistical frequency distribution verified against `numpy.histogram`.
  - `Table`: Tabular matrix visualizer with `animate_highlight_cell()`.
- **Computer Science Data Structures (`animora.datastructures`)**:
  - Independent pure Python models (`XModel`) paired with animation layers (`X`).
  - `Array`, `Stack`, `Queue`, `LinkedList`, `Heap`, `Tree`, `BST`, `Graph`, and `HashTable` (Separate Chaining).
  - Path-traced operations and complete 3-case BST deletion (leaf, 1-child, 2-children).
- **Algorithm Visualizations (`animora.algorithms`)**:
  - `OperationTrace` event recording framework.
  - `binary_search` with interval comparison tracing.
  - 5 visually distinguishable sorting algorithms: `bubble_sort`, `selection_sort`, `insertion_sort`, `merge_sort`, `quick_sort`.
  - Graph traversals: `bfs` and `dfs`.
  - Pathfinding: `dijkstra` and `a_star` with distinct exploration patterns.
  - Dynamic Programming: `fibonacci_dp` on `Table`.
  - Backtracking: `n_queens` with conflict backtracking.
- **Developer CLI (`animora.cli`)**:
  - `animora new`: Scaffold starter scene from template.
  - `animora preview`: Fast low-quality preview (`-ql`).
  - `animora render`: Production quality render (`-qh`, `-qk`).
  - `animora doctor`: System and environment diagnostics.
- **Documentation & Examples**:
  - MkDocs Material documentation site with Getting Started tutorials, subsystem guides, API reference, recipes, and troubleshooting.
  - Seven runnable, tested example scenes in `examples/`.
- **Benchmarking & Performance**:
  - Benchmark suite measuring construction, layout, and trace generation.
  - Bounding box memoization in `Component`.
