# 🧠 AI/ML Foundations & Mathematical Primitives

Animora provides declarative, high-level primitives for visualizing machine learning, mathematical optimization landscapes, vector fields, and multidimensional tensors.

---

## 1. One-Call API Ergonomics

In Animora, complex machine learning algorithms are executed and rendered via **single high-level function calls**. You never need to write manual Manim coordinate calculations or choreograph dozens of raw vector elements:

```python
from animora.core import Scene
from animora.ml import gradient_descent
from animora.theme import ModernDark, use_theme

class GradientDescentDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            # Define 2D loss surface f(x, y)
            def loss(x: float, y: float) -> float:
                return (x**2) + (y**2)

            # One-call: runs real numerical gradient descent and animates trajectory
            self.play(*gradient_descent(loss, start=(2.5, 2.5), learning_rate=0.1, steps=25))
```

---

## 2. Shared Mathematical Primitives

### `SurfacePlot`
Renders 2D contour maps and loss landscapes from arbitrary functions $f(x, y)$, automatically calculating iso-level curves and mapping coordinates via `Axes`:

```python
from animora.ml import SurfacePlot

def saddle(x: float, y: float) -> float:
    return (x**2) - (y**2)

surface = SurfacePlot(saddle, x_range=(-3, 3, 1), y_range=(-3, 3, 1), num_contours=10)
```

### `VectorField`
Renders directional vector flows and gradient arrows $-\nabla f(x, y)$ over a regular 2D grid:

```python
from animora.ml import VectorField

def neg_grad(x: float, y: float) -> tuple[float, float]:
    return -2 * x, -2 * y

vf = VectorField(neg_grad, x_range=(-2, 2, 1), y_range=(-2, 2, 1), step=0.5)
```

### `TensorGrid`
Renders 2D matrices, neural network weights, and attention heatmaps with automatic cell styling, value labeling, and cell highlight animations:

```python
import numpy as np
from animora.ml import TensorGrid

weights = np.array([[0.85, -0.42, 0.15], [0.33, 0.91, -0.78]])
grid = TensorGrid(weights, title="Layer 1 Weights")
self.play(grid.animate_create())
self.play(grid.animate_highlight_cell(0, 1))
```
