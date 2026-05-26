"""Unit tests for the Connector primitive component."""

from __future__ import annotations

import manim
import numpy as np
import pytest

from animora.components.connector import Connector
from animora.components.shape import Shape
from animora.core.animation import Animation


def test_connector_between_coordinates() -> None:
    """Verify Connector between two raw 3D coordinates."""
    p1 = [0.0, 0.0, 0.0]
    p2 = [3.0, 4.0, 0.0]
    conn = Connector(start=p1, end=p2, stroke_color="#94A3B8")

    assert np.allclose(conn.start_point, p1)
    assert np.allclose(conn.end_point, p2)
    assert isinstance(conn.manim_object, manim.Line)


def test_connector_between_components() -> None:
    """Verify Connector dynamically resolves centers from Component instances."""
    node_a = Shape.circle(radius=0.5).move_to([-2.0, 0.0, 0.0])
    node_b = Shape.circle(radius=0.5).move_to([2.0, 0.0, 0.0])

    conn = Connector(start=node_a, end=node_b)
    assert pytest.approx(conn.start_point[0], abs=1e-2) == -2.0
    assert pytest.approx(conn.end_point[0], abs=1e-2) == 2.0


def test_curved_connector() -> None:
    """Verify curved Connector constructs ArcBetweenPoints."""
    conn = Connector(start=[0, 0, 0], end=[4, 0, 0], path_arc=1.2)
    assert isinstance(conn.manim_object, manim.ArcBetweenPoints)


def test_connector_animate_draw() -> None:
    """Verify animate_draw returns valid Animation."""
    conn = Connector(start=[0, 0, 0], end=[2, 2, 0])
    anim = conn.animate_draw(run_time=1.5)
    assert isinstance(anim, Animation)
    assert anim.run_time == 1.5
    assert isinstance(anim.to_manim(), manim.Create)
