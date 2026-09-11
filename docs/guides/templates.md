# Reusable Animation Templates

Animora includes high-level presentation templates (`animora.templates`) that turn common educational animation structures into turn-key, customizable scenes.

Instead of writing boilerplate layouts, title cards, badges, and component position calculations from scratch, templates provide structured workflows with consistent proportions, typography, and visual hierarchy.

---

## 1. Available Templates

### `AlgorithmExplainerTemplate`
- **When to Use:** Explaining step-by-step algorithms (e.g. sorting algorithms, search algorithms, pathfinding) with a synchronized data structure and an educational code walk-through or stats overlay.
- **Key Parameters:**
  - `title`: Main title displayed in the header banner.
  - `subtitle`: Optional descriptive subtitle.
  - `algorithm_name`: Highlighted badge indicator (e.g., "QuickSort - O(N log N)").
  - `data`: List of items to visualize as an `Array`.

```python
from animora.core import Scene
from animora.templates import AlgorithmExplainerTemplate


class QuickSortExplainer(Scene):
    def construct(self) -> None:
        template = AlgorithmExplainerTemplate(
            title="Algorithm Deep Dive",
            subtitle="Divide and Conquer Partitioning",
            algorithm_name="QuickSort",
            data=[34, 12, 89, 5, 67, 23, 41],
        )
        template.render_scene(self)
```

---

### `DataStructureWalkthroughTemplate`
- **When to Use:** Introducing and walking through the internals of a foundational data structure (e.g., BST insertions/rotations, linked lists, queues, or hash collisions).
- **Key Parameters:**
  - `title`: Header title.
  - `ds_type`: Data structure type string (e.g. `"bst"` or `"array"`).
  - `initial_elements`: Initial elements populated in the structure.
  - `operations`: List of operations to execute (e.g. `[("insert", 25), ("insert", 60)]`).

```python
from animora.core import Scene
from animora.templates import DataStructureWalkthroughTemplate


class BSTExplainer(Scene):
    def construct(self) -> None:
        template = DataStructureWalkthroughTemplate(
            title="Binary Search Trees",
            ds_type="bst",
            initial_elements=[50, 30, 70],
            operations=[("insert", 20), ("insert", 40), ("insert", 60)],
        )
        template.render_scene(self)
```

---

### `DataComparisonTemplate`
- **When to Use:** Benchmarking or visually contrasting two or more algorithmic approaches, datasets, or performance metrics side-by-side using charts or paired structures.
- **Key Parameters:**
  - `title`: Overall comparison title.
  - `left_label`: Title for the left visual panel (e.g. `"Bubble Sort (O(N^2))"`).
  - `right_label`: Title for the right visual panel (e.g. `"Merge Sort (O(N log N))"`).
  - `left_data` & `right_data`: Data series displayed in comparative bar charts.

```python
from animora.core import Scene
from animora.templates import DataComparisonTemplate


class BenchmarkComparison(Scene):
    def construct(self) -> None:
        template = DataComparisonTemplate(
            title="Sorting Efficiency Benchmark",
            left_label="Bubble Sort (120 ops)",
            right_label="Quick Sort (28 ops)",
            left_data=[10, 25, 45, 60, 80],
            right_data=[5, 12, 18, 22, 28],
        )
        template.render_scene(self)
```

---

### `NeuralNetworkExplainerTemplate`
- **When to Use:** Visualizing multi-layer perceptrons, forward propagation, activation highlights, and layer-by-layer representations.
- **Key Parameters:**
  - `title`: Title text.
  - `subtitle`: Subtitle text.
  - `layer_sizes`: Tuple of node counts per layer (e.g., `(3, 5, 4, 2)`).
  - `activation_highlights`: Optional list of layer indices or nodes to emphasize.

```python
from animora.core import Scene
from animora.templates import NeuralNetworkExplainerTemplate


class MLPArchitectureScene(Scene):
    def construct(self) -> None:
        template = NeuralNetworkExplainerTemplate(
            title="Deep Learning Architectures",
            subtitle="Multi-Layer Perceptron Forward Pass",
            layer_sizes=(4, 6, 6, 3),
        )
        template.render_scene(self)
```

---

## 2. Customizing Templates

All templates inherit from `animora.templates.BaseTemplate`. You can override lifecycle hooks to customize animations, inject custom mobjects, or modify layouts:

1. **`build_layout()`**: Constructs header banners, labels, and bounding regions.
2. **`build_content()`**: Constructs the primary data structures or visualizations.
3. **`animate_intro(scene)`**: Plays entry transitions for header and structure.
4. **`animate_steps(scene)`**: Executes the main algorithmic or demonstration steps.
5. **`animate_outro(scene)`**: Concluding summary or exit transitions.
