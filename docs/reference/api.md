# API Reference

Complete catalog of all public modules, classes, functions, and symbols in Animora.

---

## 1. Core Module (`animora.core`)

### `Component`
Abstract base class for all visual and composite components.
- `@property manim_object -> manim.Mobject`: Access the underlying Manim object.
- `@property center -> tuple[float, float, float]`: Bounding box center coordinates.
- `@property width / height / depth -> float`: Geometric dimensions.
- `move_to(point) -> Self`: Position component at 3D coordinate vector.
- `animate_fade_in(run_time) -> Animation`: Fade-in animation.
- `animate_create(run_time) -> Animation`: Draw/create animation.

### `Scene`
Wrapper around Manim Scene supporting polymorphic `.play()` execution.
- `play(*animations_or_components, **kwargs)`: Play Animora animations or Manim animations.

### `Animation`
Polymorphic bridge wrapping Manim animations.

---

## 2. Visual Primitives (`animora.components`)

- `Text(text, font_size=None, color=None, font=None)`: Styled typography.
- `Shape.circle(radius, fill_color, stroke_color)`: Circle shape.
- `Shape.rectangle(width, height, fill_color)`: Rectangle shape.
- `Shape.rounded_rectangle(width, height, corner_radius)`: Rounded rectangle.
- `Connector(start, end, path_arc, stroke_color)`: Connecting line or arc.
- `Arrow(start, end, path_arc, tip_length)`: Directional arrow.
- `Group(*children)`: Composite container with `arrange(layout)`.
- `Panel(*children, title=None, padding=None)`: Padded container card.

---

## 3. Layout Engines (`animora.layout`)

- `HorizontalLayout(spacing=0.2, alignment="center")`
- `VerticalLayout(spacing=0.2, alignment="center")`
- `GridLayout(columns=3, col_spacing=0.2, row_spacing=0.2)`
- `CircularLayout(radius=2.0, start_angle=0.0)`
- `TreeLayout(root_id, tree_hierarchy, level_height=1.2)`
- `GraphLayout(nodes, edges, algorithm="spring", scale=3.0)`
- `FlowLayout(step_spacing=0.5, max_per_line=4)`

---

## 4. Theming (`animora.theme`)

- `Theme(name, colors, typography, spacing, strokes, corner_radius, timing)`
- `use_theme(theme: Theme)`: Context manager for scoped styling.
- Built-in Themes: `ModernDark`, `PaperLight`, `Cyberpunk`, `Monokai`, `DefaultTheme`.

---

## 5. Data Visualization (`animora.dataviz`)

- `Axes(x_range, y_range, x_length, y_length)`: 2D coordinate system with `c2p()` and `p2c()`.
- `BarChart(data, axes=None, bar_width=0.6)`: Bar chart with `animate_grow()`.
- `LineChart(points, axes=None, show_dots=True)`: Line chart with `animate_draw()`.
- `ScatterPlot(points, axes=None, point_radius=0.1)`: Scatter plot with `animate_plot()`.
- `Histogram(data, bins=10, axes=None)`: Statistical histogram with `animate_grow()`.
- `Table(data, headers=None, cell_width=2.2)`: Grid table with `animate_highlight_cell()`.

---

## 6. Data Structures (`animora.datastructures`)

- `Array(values, show_indices=True)`: `animate_swap()`, `animate_highlight()`, `animate_set()`.
- `Stack(items)`: `animate_push()`, `animate_pop()`, `animate_peek()`.
- `Queue(items)`: `animate_enqueue()`, `animate_dequeue()`, `animate_peek()`.
- `LinkedList(values)`: `animate_insert_tail()`.
- `Heap(values)`: `animate_insert()`, `animate_extract()`.
- `Tree(root_value)`: `animate_highlight_node()`.
- `BST(values)`: `animate_insert()`, `animate_search()`, `animate_delete()`.
- `Graph(nodes, edges, directed=False)`: `animate_highlight_node()`, `animate_mark_visited()`, `animate_highlight_edge()`.
- `HashTable(num_buckets=5)`: `animate_insert()`, `animate_search()`.

---

## 7. Algorithms (`animora.algorithms`)

- `binary_search(arr, target) -> list[Animation]`
- `bubble_sort(arr) -> list[Animation]`
- `selection_sort(arr) -> list[Animation]`
- `insertion_sort(arr) -> list[Animation]`
- `merge_sort(arr) -> list[Animation]`
- `quick_sort(arr) -> list[Animation]`
- `bfs(graph, start) -> list[Animation]`
- `dfs(graph, start) -> list[Animation]`
- `dijkstra(graph, start, target) -> list[Animation]`
- `a_star(graph, start, goal, heuristic) -> list[Animation]`
- `fibonacci_dp(n, table) -> list[Animation]`
- `n_queens(n, table) -> list[Animation]`
