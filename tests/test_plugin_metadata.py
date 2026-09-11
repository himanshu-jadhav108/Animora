"""Tests for Manim plugin entry points and packaging discoverability metadata."""

from __future__ import annotations

import sys
from importlib.metadata import entry_points

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
from pathlib import Path


def test_manim_plugin_entry_point_registered() -> None:
    """Verify that Animora is registered under the 'manim.plugins' entry point group."""
    eps = entry_points(group="manim.plugins")
    plugin_names = [ep.name for ep in eps]
    assert "animora" in plugin_names, (
        f"Expected 'animora' in manim.plugins entry points, got: {plugin_names}"
    )

    # Verify that the entry point loads cleanly
    animora_ep = next(ep for ep in eps if ep.name == "animora")
    loaded = animora_ep.load()
    assert hasattr(loaded, "__version__")
    assert hasattr(loaded, "Scene")
    assert hasattr(loaded, "Component")


def test_pyproject_discoverability_metadata() -> None:
    """Verify pyproject.toml contains required keywords and classifiers for discoverability."""
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    assert pyproject_path.is_file()

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    project = data.get("project", {})

    # Check keywords
    keywords = project.get("keywords", [])
    expected_keywords = {"manim", "animation", "visualization", "education", "algorithms"}
    for kw in expected_keywords:
        assert kw in keywords, f"Keyword '{kw}' missing from pyproject.toml"

    # Check classifiers
    classifiers = project.get("classifiers", [])
    assert any("Topic :: Multimedia :: Graphics" in c for c in classifiers)
    assert any("Topic :: Scientific/Engineering :: Visualization" in c for c in classifiers)

    # Check entry point definition
    entry_points_table = project.get("entry-points", {})
    manim_plugins = entry_points_table.get("manim.plugins", {})
    assert manim_plugins.get("animora") == "animora"
