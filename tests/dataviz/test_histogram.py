"""Unit tests for Histogram data visualization component verifying against NumPy reference."""

from __future__ import annotations

import numpy as np
import pytest
from animora.dataviz.histogram import Histogram


def test_histogram_verified_against_numpy() -> None:
    """Verify statistical binning matches numpy.histogram exactly."""
    np.random.seed(42)
    sample_data = np.random.normal(loc=5.0, scale=2.0, size=100)

    # Animora calculation
    anim_counts, anim_edges = Histogram.compute_histogram(sample_data, bins=8)

    # Reference NumPy calculation
    np_counts, np_edges = np.histogram(sample_data, bins=8)

    assert np.array_equal(anim_counts, np_counts)
    assert np.allclose(anim_edges, np_edges, atol=1e-6)


def test_histogram_component_construction() -> None:
    """Verify Histogram component builds bars matching bin count."""
    data = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    hist = Histogram(data=data, bins=4)

    assert len(hist.counts) == 4
    assert len(hist._bars) == 4
    assert sum(hist.counts) == len(data)
