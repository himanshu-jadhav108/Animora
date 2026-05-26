"""Unit tests for the Group composite component."""

from __future__ import annotations

import manim
import numpy as np
import pytest

from animora.components.group import Group
from animora.components.shape import Shape
from animora.components.text import Text


def test_group_construction_and_indexing() -> None:
    """Verify Group wraps children and supports indexing, length, and iteration."""
    c1 = Shape.circle(radius=0.5)
    t1 = Text("Node")
    grp = Group(c1, t1)

    assert len(grp) == 2
    assert grp[0] is c1
    assert grp[1] is t1
    assert list(grp) == [c1, t1]
    assert isinstance(grp.manim_object, (manim.VGroup, manim.Group))


def test_group_collective_transformations() -> None:
    """Verify moving and shifting Group transforms all children."""
    c1 = Shape.circle(radius=0.5).move_to([0, 0, 0])
    c2 = Shape.circle(radius=0.5).move_to([2, 0, 0])
    grp = Group(c1, c2)

    grp.shift([0, 3, 0])
    assert pytest.approx(c1.center[1], abs=1e-2) == 3.0
    assert pytest.approx(c2.center[1], abs=1e-2) == 3.0


def test_group_add_and_remove() -> None:
    """Verify dynamic add and remove on Group."""
    c1 = Shape.circle()
    c2 = Shape.circle()
    grp = Group(c1)

    grp.add(c2)
    assert len(grp) == 2
    assert c2 in grp.children

    grp.remove(c1)
    assert len(grp) == 1
    assert c1 not in grp.children
