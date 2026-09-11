"""Unit tests for Animora named animation timing and easing presets."""

from __future__ import annotations

import pytest

from animora.theme import (
    CINEMATIC,
    EDUCATIONAL,
    PLAYFUL,
    SLOW_MO,
    SMOOTH,
    SNAPPY,
    TimingPreset,
    get_timing_preset,
)


def test_canonical_presets_properties() -> None:
    """Verify that all canonical presets have positive durations and valid rate funcs."""
    for preset in [SNAPPY, SMOOTH, CINEMATIC, PLAYFUL, EDUCATIONAL, SLOW_MO]:
        assert isinstance(preset, TimingPreset)
        assert preset.duration > 0
        assert callable(preset.rate_func)
        assert len(preset.name) > 0
        assert len(preset.description) > 0


def test_get_timing_preset_lookup() -> None:
    """Verify lookup by string key and by direct preset pass-through."""
    assert get_timing_preset("snappy") is SNAPPY
    assert get_timing_preset("CINEMATIC") is CINEMATIC
    assert get_timing_preset("slow-mo") is SLOW_MO
    assert get_timing_preset(SMOOTH) is SMOOTH

    with pytest.raises(KeyError, match="Unknown timing preset 'non_existent'"):
        get_timing_preset("non_existent")


def test_preset_apply_to_kwargs() -> None:
    """Verify applying a preset fills run_time and rate_func only when unset."""
    kwargs: dict[str, object] = {}
    applied = SNAPPY.apply_to_kwargs(kwargs)
    assert applied["run_time"] == SNAPPY.duration
    assert applied["rate_func"] == SNAPPY.rate_func

    # Explicit override takes precedence
    custom_kwargs: dict[str, object] = {"run_time": 9.9}
    applied_custom = SNAPPY.apply_to_kwargs(custom_kwargs)
    assert applied_custom["run_time"] == 9.9
    assert applied_custom["rate_func"] == SNAPPY.rate_func
