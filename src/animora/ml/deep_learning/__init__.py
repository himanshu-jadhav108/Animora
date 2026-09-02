"""Deep learning models, visualizers, and one-call animation APIs."""

from __future__ import annotations

from animora.ml.deep_learning.backpropagation import (
    BackpropagationModel,
    BackpropagationVisualizer,
    backpropagation,
)
from animora.ml.deep_learning.cnn_convolution import (
    CNNConvolutionModel,
    CNNConvolutionVisualizer,
    cnn_convolution,
)
from animora.ml.deep_learning.neural_network import (
    NeuralNetworkModel,
    NeuralNetworkVisualizer,
    neural_network_forward,
)
from animora.ml.deep_learning.optimizers import (
    AdamOptimizerModel,
    BaseOptimizerModel,
    MomentumOptimizerModel,
    OptimizerVisualizer,
    SGDOptimizerModel,
    adam,
    momentum,
    sgd,
)
from animora.ml.deep_learning.rnn_cell import (
    RNNCellModel,
    RNNVisualizer,
    rnn_forward,
)

__all__ = [
    "AdamOptimizerModel",
    "BackpropagationModel",
    "BackpropagationVisualizer",
    "BaseOptimizerModel",
    "CNNConvolutionModel",
    "CNNConvolutionVisualizer",
    "MomentumOptimizerModel",
    "NeuralNetworkModel",
    "NeuralNetworkVisualizer",
    "OptimizerVisualizer",
    "RNNCellModel",
    "RNNVisualizer",
    "SGDOptimizerModel",
    "adam",
    "backpropagation",
    "cnn_convolution",
    "momentum",
    "neural_network_forward",
    "rnn_forward",
    "sgd",
]
