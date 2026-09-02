# Machine Learning & AI Visualization — One-Call API Contract

## 1. Executive Summary

This document establishes the binding architectural contract for all Machine Learning, Deep Learning, and Natural Language Processing components in `animora.ml` (Phases 13a through 13e).

### The Prime Directive: Zero Raw Manim for the User
A user visualizing ML concepts must **never write raw Manim coordinate calculations or manually sequence dozens of `self.play()` calls**. Every capability across ML/DL/NLP must be fully usable as a **single high-level call**, returning everything needed to execute `self.play(...)`:

```python
# 1-Line Clean Ergonomic:
self.play(*gradient_descent(loss_fn, start=(3.0, 3.0), learning_rate=0.1, steps=30))
```

---

## 2. Core Design Principles

### Principle 1: One-Call Ergonomics
1. Every component in `animora.ml` exposes a high-level one-call method (e.g. `.animate(...)` or top-level function) that executes the complete domain visualization.
2. The user passes high-level domain data (loss functions, dataset arrays, weights, attention scores, network layers).
3. The component handles layout positioning, color scales, vector mapping, and step-by-step animation generation automatically.

### Principle 2: Dual-Correctness & Operation Tracing
1. **Computational Correctness**: Animations must be driven by real mathematical algorithms running on real data (NumPy-based gradients, real loss calculations, actual matrix products), never hardcoded or visual illusions.
2. **Operation Tracing**: Mathematical execution records an `MLTrace` / `OperationTrace` of discrete steps $(x_k, y_k, \mathcal{L}, \nabla \mathcal{L})$.
3. **Visual Correctness**: Animation sequences are verified against the recorded mathematical trace step-by-step.

### Principle 3: Primitive & Layout Reuse
No component in `animora.ml` shall reinvent:
- Coordinate mapping $\rightarrow$ Reuse `animora.dataviz.Axes` (`c2p`, `p2c`).
- Directional vectors $\rightarrow$ Reuse `animora.components.Arrow`.
- Matrix & grid layouts $\rightarrow$ Reuse `animora.layout.GridLayout`.
- Visual cards & text $\rightarrow$ Reuse `animora.components.Panel`, `Shape`, `Text`.
- Color palettes $\rightarrow$ Reuse `animora.theme.get_active_theme()`.

---

## 3. Class Hierarchy & Base Contract

```
Component (animora.core.component)
  └── MLComponent (animora.ml.base)
        ├── SurfacePlot (animora.ml.surface_plot)
        ├── VectorField (animora.ml.vector_field)
        ├── TensorGrid (animora.ml.tensor_grid)
        └── GradientDescentVisualizer (animora.ml.optimization.gradient_descent)
```

### Base Class Interface (`animora.ml.base.MLComponent`):
```python
class MLComponent(Component):
    """Base class for all Machine Learning visual components."""

    def animate_create(self, run_time: float | None = None) -> Animation:
        """Construct the visual representation in the scene."""
        ...
```

---

## 4. Sub-Phase Roadmap Adherence

- **Phase 13a**: Foundations, One-Call Contract, `SurfacePlot`, `VectorField`, `TensorGrid`, and `GradientDescent`.
- **Phase 13b**: Classic ML (Linear/Logistic Regression, K-Means, PCA, SVM, Decision Boundaries).
- **Phase 13c**: Deep Learning (MLP Neural Networks, Forward/Backward Passes, Activation Functions, CNN Filters, RNN Unrolling).
- **Phase 13d**: NLP & Transformers (Tokenization, Embeddings, Scaled Dot-Product Attention Heatmaps, Transformer Block Flow).
- **Phase 13e**: Documentation, Interactive Gallery Showcase, and End-to-End Guides.
