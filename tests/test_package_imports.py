"""Smoke tests verifying that all Animora subpackages import cleanly."""

from __future__ import annotations

import importlib

import pytest


def test_import_animora_root() -> None:
    """Verify that the root animora package imports and defines version."""
    import animora

    assert hasattr(animora, "__version__")
    assert isinstance(animora.__version__, str)


@pytest.mark.parametrize(
    "submodule",
    [
        "animora.core",
        "animora.components",
        "animora.components.primitives",
        "animora.components.dataviz",
        "animora.components.dsa",
        "animora.layout",
        "animora.theme",
        "animora.animations",
        "animora.cli",
    ],
)
def test_import_submodules(submodule: str) -> None:
    """Verify that each architectural module defined in Phase 0 imports without error."""
    mod = importlib.import_module(submodule)
    assert mod is not None
    assert hasattr(mod, "__all__")
