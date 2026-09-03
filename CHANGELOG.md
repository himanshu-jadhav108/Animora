# Changelog

All notable changes to the **Animora** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0a1] - 2026-09-03

### Added
- **AI & Machine Learning Foundations (`animora.ml`)**:
  - `SurfacePlot`: 2D continuous contour elevation and iso-level visualization for scalar loss surfaces $f(x, y)$.
  - `VectorField`: Regular 2D directional flow vector field and gradient arrows $-\nabla f(x, y)$.
  - `TensorGrid`: Interactive matrix heatmap visualizer with individual cell styling, value labeling, and cell highlight animations.
  - `gradient_descent`: One-call numerical optimization engine on 2D loss surfaces with full diagnostic trajectory tracing.
  - `MLComponent`, `MLTrace`, and `MLTraceStep` base contracts establishing pure numerical execution separated from animation choreography.
- **Classic Machine Learning (`animora.ml.classic`)**:
  - `linear_regression`: Analytical least-squares fit $(X^T X)^{-1} X^T y$ with dynamic line tracking during gradient descent.
  - `logistic_regression`: Binary cross-entropy classifier showing sigmoid probabilities and shifting decision boundary $w^T x + b = 0$.
  - `kmeans`: Lloyd's algorithm with centroid translation and Voronoi sample recoloring.
  - `decision_tree`: Recursive Gini impurity / Shannon entropy tree partitioning visualized via `TreeLayout` and `Panel` cards.
  - `svm`: Hard-margin support vector machine with hyperplane $w \cdot x + b = 0$, dashed margin boundaries $w \cdot x + b = \pm 1$, and support vector highlights.
  - `pca`: Covariance eigendecomposition via `numpy.linalg.eigh`, drawing principal eigenvectors from the centroid and projecting samples orthogonally.
- **Deep Learning & Gradients (`animora.ml.deep_learning`)**:
  - `neural_network_forward`: Layered multi-layer perceptron architecture with animated activations propagating layer-by-layer.
  - `backpropagation`: Exact analytical gradient computation ($\partial \mathcal{L}/\partial W$, $\partial \mathcal{L}/\partial b$) verified against finite-difference numerical checks ($2.28 \times 10^{-11}$ relative error) with reverse gradient wave animation.
  - `optimizers` (`sgd`, `momentum`, `adam`): Numerical optimization algorithms comparing inertia and adaptive moment trajectories over anisotropic loss surfaces.
  - `cnn_convolution`: 2D sliding-window convolution operation showing kernel dot products populating feature map cells.
  - `rnn_forward`: Unrolled recurrent neural network cell showing the hidden state recurrence relation $h_t = \tanh(W_{xh} x_t + W_{hh} h_{t-1} + b_h)$.
- **NLP & Attention Mechanisms (`animora.ml.nlp`)**:
  - `tokenize`: Regex tokenizer extracting tokens and character spans, animating raw strings separating into bordered badge chips.
  - `word_embeddings`: Illustrative $D$-dimensional embedding table with 2D PCA projection reuse.
  - `attention`: Scaled dot-product attention $\text{softmax}(Q K^T / \sqrt{d_k}) V$ with mathematically verified row-wise normalization ($1.0 \pm 10^{-6}$).
  - `transformer_block`: Minimal single-head attention and ReLU feedforward network composition with transparent pedagogical scope.
- **Documentation Site & Responsive Media (Phase 10.5 & 13e)**:
  - Promoted "AI & Machine Learning" to a dedicated top-level navigation section.
  - Added section landing page (`docs/ml/index.md`) with a 4-stage sequential learning path.
  - Created 19 responsive SVG vector assets in `docs/assets/media/` that scale smoothly across mobile, tablet, and desktop viewports.
  - Added responsive CSS media queries in `docs/stylesheets/extra.css` for cross-device styling.
  - Complete API reference coverage in `docs/reference/api.md` with zero undocumented public symbols.
  - Added automated documentation integrity test script `scripts/verify_docs_integrity.py`.
- **Runnable Example Scripts (`examples/`)**:
  - `08_ai_ml_foundations.py`: Surface plots and gradient descent.
  - `09_classic_machine_learning.py`: Analytical linear regression.
  - `10_deep_learning_and_backprop.py`: Neural network forward pass.
  - `11_nlp_and_attention.py`: String tokenization into chips.

### Changed
- Generalized `PCAModel` dimension validation to accept arbitrary $D \ge 2$ features for multi-dimensional projection reuse.
- Updated README badges, author profile card, and documentation links.

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
