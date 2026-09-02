"""Verification that SGD, Momentum, and Adam produce demonstrably distinct traces."""

from __future__ import annotations

import numpy as np

from animora.core.animation import Animation
from animora.ml.deep_learning.optimizers import (
    AdamOptimizerModel,
    MomentumOptimizerModel,
    SGDOptimizerModel,
    adam,
    momentum,
    sgd,
)


def anisotropic_loss(x: float, y: float) -> float:
    """Anisotropic ravine: steep along x, shallow along y."""
    return 10.0 * (x**2) + (y**2)


def test_optimizers_behavioral_distinction() -> None:
    """Explicitly verify that SGD, Momentum, and Adam produce distinct optimization traces."""
    start_point = (2.0, 2.0)
    steps = 15

    sgd_model = SGDOptimizerModel(
        anisotropic_loss, start=start_point, learning_rate=0.06, steps=steps
    )
    sgd_traj = np.array([p[:2] for p in sgd_model.optimize()])

    mom_model = MomentumOptimizerModel(
        anisotropic_loss, start=start_point, learning_rate=0.06, momentum=0.8, steps=steps
    )
    mom_traj = np.array([p[:2] for p in mom_model.optimize()])

    adam_model = AdamOptimizerModel(
        anisotropic_loss, start=start_point, learning_rate=0.3, steps=steps
    )
    adam_traj = np.array([p[:2] for p in adam_model.optimize()])

    # 1. Check shapes match
    assert len(sgd_traj) == steps + 1
    assert len(mom_traj) == steps + 1
    assert len(adam_traj) == steps + 1

    # 2. Verify Momentum trajectory differs significantly from SGD (due to inertia)
    mom_diff = float(np.mean(np.linalg.norm(mom_traj - sgd_traj, axis=1)))
    assert mom_diff > 0.2, f"Momentum trace did not meaningfully diverge from SGD: {mom_diff}"

    # 3. Verify Adam trajectory differs significantly from SGD (due to adaptive moments)
    adam_diff = float(np.mean(np.linalg.norm(adam_traj - sgd_traj, axis=1)))
    assert adam_diff > 0.2, f"Adam trace did not meaningfully diverge from SGD: {adam_diff}"

    # 4. Verify Momentum and Adam also differ from each other
    mom_adam_diff = float(np.mean(np.linalg.norm(mom_traj - adam_traj, axis=1)))
    assert mom_adam_diff > 0.2

    # 5. Check trace events contain optimizer-specific diagnostic fields
    assert "gradient" in sgd_model.trace[0].values
    assert "velocity" in mom_model.trace[0].values
    assert "m" in adam_model.trace[0].values
    assert "v" in adam_model.trace[0].values


def test_optimizers_one_call_apis() -> None:
    def loss(x: float, y: float) -> float:
        return x**2 + y**2

    anims_sgd = sgd(loss, steps=3)
    assert len(anims_sgd) >= 2
    assert all(isinstance(a, Animation) for a in anims_sgd)

    anims_mom = momentum(loss, steps=3)
    assert len(anims_mom) >= 2

    anims_adam = adam(loss, steps=3)
    assert len(anims_adam) >= 2
