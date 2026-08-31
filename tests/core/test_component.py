"""Unit tests for the Component base class, geometry, positioning, and escape hatch."""

from __future__ import annotations

from typing import Any

import manim
import numpy as np
import pytest

from animora.core.animation import Animation
from animora.core.component import Component


class DummyBoxComponent(Component):
    """Concrete dummy component for testing base Component methods."""

    def __init__(self, width: float = 2.0, height: float = 1.0, **kwargs: Any) -> None:
        self._box_width = width
        self._box_height = height
        super().__init__(**kwargs)

    def _build_mobject(self) -> manim.Mobject:
        return manim.Rectangle(width=self._box_width, height=self._box_height, color=manim.BLUE)


def test_escape_hatch_access() -> None:
    """Verify .manim_object escape hatch returns the underlying Manim Mobject."""
    comp = DummyBoxComponent(width=3.0, height=2.0)
    mob = comp.manim_object

    assert isinstance(mob, manim.Mobject)
    assert isinstance(mob, manim.Rectangle)
    # Consecutive calls return the exact same instance
    assert comp.manim_object is mob


def test_geometric_dimensions() -> None:
    """Verify width, height, depth, center, and bounding box properties."""
    comp = DummyBoxComponent(width=4.0, height=2.0)
    assert pytest.approx(comp.width, abs=1e-3) == 4.0
    assert pytest.approx(comp.height, abs=1e-3) == 2.0
    assert isinstance(comp.center, np.ndarray)

    bbox = comp.bounding_box
    assert pytest.approx(bbox.width, abs=1e-3) == 4.0
    assert pytest.approx(bbox.height, abs=1e-3) == 2.0


def test_spatial_positioning_and_chaining() -> None:
    """Verify move_to, shift, scale, and fluent method chaining."""
    comp1 = DummyBoxComponent(width=2.0, height=1.0)
    comp2 = DummyBoxComponent(width=2.0, height=1.0)

    # Fluent move_to
    res = comp1.move_to(np.array([2.0, 3.0, 0.0]))
    assert res is comp1
    assert np.allclose(comp1.center, [2.0, 3.0, 0.0], atol=1e-3)

    # Shift
    comp1.shift(np.array([-1.0, 0.0, 0.0]))
    assert np.allclose(comp1.center, [1.0, 3.0, 0.0], atol=1e-3)

    # next_to
    comp2.next_to(comp1, direction=manim.RIGHT, buff=0.5)
    assert comp2.center[0] > comp1.center[0]

    # scale
    old_width = comp1.width
    comp1.scale(2.0)
    assert pytest.approx(comp1.width, abs=1e-3) == old_width * 2.0


def test_semantic_animation_generators() -> None:
    """Verify animate_create, animate_fade_in, and animate_fade_out generators."""
    comp = DummyBoxComponent()

    create_anim = comp.animate_create(run_time=1.5)
    assert isinstance(create_anim, Animation)
    assert create_anim.name == "create"
    assert create_anim.run_time == 1.5

    fade_in_anim = comp.animate_fade_in(run_time=0.8)
    assert isinstance(fade_in_anim, Animation)
    assert fade_in_anim.name == "fade_in"

    fade_out_anim = comp.animate_fade_out(run_time=0.5)
    assert isinstance(fade_out_anim, Animation)
    assert fade_out_anim.name == "fade_out"
