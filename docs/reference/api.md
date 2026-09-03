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

---

## 8. AI & Machine Learning (`animora.ml`)

### Core & Base Architecture
- `MLComponent`: Abstract base class for machine learning visualizers pairing models with animation layers.
- `MLTrace`: Immutable sequential execution trace of algorithm diagnostics and state changes.
- `MLTraceStep`: Diagnostic step entry containing timestamp, name, description, and state dictionary.

### Mathematical Foundations & Optimization
- `SurfacePlot(func, x_range, y_range, num_contours)`: 2D contour map for scalar functions $f(x, y)$.
- `VectorField(vector_func, x_range, y_range, step)`: 2D directional flow vector field.
- `TensorGrid(matrix, title=None, cell_size=0.8)`: Heatmap grid for weights, matrices, and tensors.
- `GradientDescentModel(func, grad_func=None, start=(0,0), learning_rate=0.1, steps=20)`: Pure numerical optimization engine.
- `GradientDescentVisualizer(func, start, learning_rate, steps)`: Visualizer pairing surface contours with trajectory dots.
- `gradient_descent(func, start, learning_rate=0.1, steps=20) -> list[Animation]`: One-call optimization animation.

### Classic Machine Learning (`animora.ml.classic`)
- `LinearRegressionModel(x, y)`: Analytical least-squares fit $(X^TX)^{-1}X^Ty$ and gradient tracking.
- `LinearRegressionVisualizer(x, y, steps=10)`: Plots scatter points and converges fitting line.
- `linear_regression(x, y, steps=10) -> list[Animation]`: One-call linear regression animation.
- `LogisticRegressionModel(X, y, lr=0.1, steps=20)`: Cross-entropy binary classifier.
- `LogisticRegressionVisualizer(X, y, steps=10)`: Plots 2D classes and shifts decision boundary $w^Tx + b = 0$.
- `logistic_regression(X, y, steps=10) -> list[Animation]`: One-call logistic regression animation.
- `KMeansModel(data, k=3, max_iters=10)`: Lloyd's clustering algorithm.
- `KMeansVisualizer(data, k=3, max_iters=10)`: Plots cluster samples and translates centroids.
- `kmeans(data, k=3, max_iters=10) -> list[Animation]`: One-call K-Means clustering animation.
- `DecisionNode`, `DecisionTreeModel(X, y, max_depth=3, criterion="gini")`: Exact split decision tree.
- `DecisionTreeVisualizer(X, y, max_depth=3)`: Renders tree nodes and split edges via `TreeLayout`.
- `decision_tree(X, y, max_depth=3) -> list[Animation]`: One-call decision tree animation.
- `HardMarginSVMModel(X, y)`: Primal hard-margin hyperplane and support vector solver.
- `SVMVisualizer(X, y)`: Visualizes separating hyperplane, margin bounds $w\cdot x + b = \pm 1$, and support vectors.
- `svm(X, y) -> list[Animation]`: One-call SVM animation.
- `PCAModel(X, n_components=2)`: Covariance eigendecomposition via `numpy.linalg.eigh`.
- `PCAVisualizer(X, n_components=1)`: Visualizes principal eigenvector arrows and orthogonal projections.
- `pca(X, n_components=1) -> list[Animation]`: One-call PCA animation.

### Deep Learning (`animora.ml.deep_learning`)
- `NeuralNetworkModel(layer_sizes, activation="sigmoid")`: Layered feedforward architecture.
- `NeuralNetworkVisualizer(layer_sizes, input_data)`: Renders nodes, synapses, and activation pulses.
- `neural_network_forward(layer_sizes, input_data, activation="sigmoid") -> list[Animation]`: One-call forward pass animation.
- `BackpropagationModel(model, input_data, target_data, lr=0.1)`: Analytical gradient computation with finite-difference check.
- `BackpropagationVisualizer(model, input_data, target_data)`: Animates forward pass followed by backward gradient wave.
- `backpropagation(model, input_data, target_data) -> list[Animation]`: One-call backpropagation animation.
- `BaseOptimizerModel`, `SGDOptimizerModel`, `MomentumOptimizerModel`, `AdamOptimizerModel`: Pure NumPy optimizers.
- `OptimizerVisualizer(func, optimizer, start, steps)`: Animates parameter trajectories over loss surfaces.
- `sgd(func, start, lr=0.1, steps=20) -> list[Animation]`: One-call SGD optimization.
- `momentum(func, start, lr=0.1, beta=0.9, steps=20) -> list[Animation]`: One-call Polyak Momentum optimization.
- `adam(func, start, lr=0.1, beta1=0.9, beta2=0.999, steps=20) -> list[Animation]`: One-call Adam optimization.
- `CNNConvolutionModel(input_matrix, kernel, stride=1, padding=0)`: 2D sliding-window convolution engine.
- `CNNConvolutionVisualizer(input_matrix, kernel, stride=1)`: Visualizes sliding kernel box and feature map cell population.
- `cnn_convolution(input_matrix, kernel, stride=1) -> list[Animation]`: One-call 2D convolution animation.
- `RNNCellModel(input_dim, hidden_dim)`: Unrolled recurrent hidden state computation $h_t = \tanh(W_{xh}x_t + W_{hh}h_{t-1} + b_h)$.
- `RNNVisualizer(sequence, hidden_dim)`: Animates unrolled timesteps, input injections, and hidden state transitions.
- `rnn_forward(sequence, hidden_dim=2) -> list[Animation]`: One-call RNN sequence animation.

### NLP & Attention (`animora.ml.nlp`)
- `TokenizerModel(text)`: Regex tokenizer preserving tokens and character spans.
- `TokenizerVisualizer(text)`: Animates raw text separating into token chip badges.
- `tokenize(text) -> list[Animation]`: One-call tokenization animation.
- `EmbeddingModel(tokens, embed_dim=4)`: Discrete tokens to illustrative vector space with 2D PCA projection.
- `EmbeddingVisualizer(tokens, embed_dim=4)`: Renders 2D projected embedding scatter points.
- `word_embeddings(tokens, embed_dim=4) -> list[Animation]`: One-call word embedding animation.
- `AttentionModel(inputs, d_k=2)`: Scaled dot-product attention $A = \text{softmax}(QK^T / \sqrt{d_k}) V$.
- `AttentionVisualizer(inputs, d_k=2)`: Renders $Q, K, V$ matrices, attention heatmap grid, and context output.
- `attention(inputs, d_k=2) -> list[Animation]`: One-call attention animation.
- `TransformerBlockModel(inputs, d_k=2, d_ff=4)`: Self-attention and ReLU feedforward composition.
- `TransformerBlockVisualizer(inputs, d_k=2, d_ff=4)`: Visualizes sequential transformer sublayers.
- `transformer_block(inputs, d_k=2, d_ff=4) -> list[Animation]`: One-call transformer block animation.
