# 🧠 Deep Learning Visualizations

Animora provides one-call, dual-correctness visualizers for foundational deep learning components. Every model computes real NumPy activations, exact analytical gradients, and tensor manipulations—verified against numerical ground truths without external framework dependencies.

---

## 1. Neural Network Structure & Forward Pass

Renders a multi-layer perceptron architecture and animates activations propagating layer-by-layer:

```python
from animora.core import Scene
from animora.ml.deep_learning import neural_network_forward
from animora.theme import ModernDark, use_theme

class NeuralNetDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            # Animates layered architecture and forward pass
            self.play(*neural_network_forward(
                layer_sizes=[2, 3, 1],
                input_data=[0.8, -0.4],
                activation="sigmoid",
            ))
```

---

## 2. Backpropagation Gradient Flow

Computes analytical gradients $\frac{\partial \mathcal{L}}{\partial W}$ and $\frac{\partial \mathcal{L}}{\partial b}$ (verified against finite-difference gradient checks with relative error $< 10^{-5}$) and animates a reverse gradient wave flowing from the loss back to the inputs:

```python
from animora.core import Scene
from animora.ml.deep_learning import NeuralNetworkModel, backpropagation
from animora.theme import ModernDark, use_theme

class BackpropDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            net = NeuralNetworkModel(layer_sizes=[2, 3, 1], activation="sigmoid")

            # Animates forward pass followed by backward gradient flow
            self.play(*backpropagation(net, input_data=[0.6, 0.2], target_data=[1.0]))
```

---

## 3. Optimizers: SGD, Momentum, Adam

Animates optimization trajectories over non-convex or anisotropic loss surfaces:

```python
from animora.core import Scene
from animora.ml.deep_learning import adam, momentum, sgd
from animora.theme import ModernDark, use_theme

def rosenbrock(x: float, y: float) -> float:
    return (1.0 - x)**2 + 10.0 * (y - x**2)**2

class OptimizersDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            # Compare optimizer dynamics on a shared loss surface
            self.play(*sgd(rosenbrock, start=(2.0, 2.0), steps=20))
            self.play(*momentum(rosenbrock, start=(2.0, 2.0), steps=20))
            self.play(*adam(rosenbrock, start=(2.0, 2.0), steps=20))
```

---

## 4. CNN 2D Convolution Operation

Visualizes a sliding window bounding box moving across an input matrix, computing elementwise dot products with the kernel, and populating the output feature map:

```python
from animora.core import Scene
from animora.ml.deep_learning import cnn_convolution
from animora.theme import ModernDark, use_theme

class ConvolutionDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            image = [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0],
            ]
            kernel = [
                [1.0, 0.0],
                [0.0, 1.0],
            ]

            self.play(*cnn_convolution(image, kernel, stride=1))
```

---

## 5. RNN Sequential State Updates

Renders an unrolled recurrent neural network cell showing the hidden state recurrence relation $h_t = \tanh(W_{xh} x_t + W_{hh} h_{t-1} + b_h)$ across timesteps:

```python
from animora.core import Scene
from animora.ml.deep_learning import rnn_forward
from animora.theme import ModernDark, use_theme

class RNNDemo(Scene):
    def construct(self) -> None:
        with use_theme(ModernDark):
            sequence = [
                [1.0, 0.5],
                [0.2, 0.8],
                [-0.4, 0.1],
            ]

            self.play(*rnn_forward(sequence, hidden_dim=2))
```

---

## 📌 Scope Boundaries & Future Sub-Phases

Animora deep learning visualizers are strictly scoped for pedagogical transparency:
- **No Heavyweight Frameworks**: Everything runs on pure NumPy arithmetic.
- **Isolated Operations**: Designed for single passes and demonstrative parameter updates rather than full end-to-end multi-epoch training loops.
- **Attention & Transformers**: Reserved for **Phase 13d**.
