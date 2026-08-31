"""Unit tests for the Panel card container component."""

from __future__ import annotations

import manim

from animora.components.panel import Panel
from animora.components.text import Text


def test_panel_construction_with_children() -> None:
    """Verify Panel wraps children and calculates bounding dimensions."""
    t1 = Text("Panel Content", font_size=24)
    panel = Panel(t1, title="Header", padding=0.5)

    assert panel.title is not None
    assert panel.title.text == "Header"
    assert len(panel.content) == 1
    assert isinstance(panel.manim_object, manim.VGroup)
    # Background width must be at least content width + padding
    assert panel.width >= t1.width + 0.5


def test_panel_empty_fallback_dimensions() -> None:
    """Verify Panel without children constructs with default minimal sizing."""
    panel = Panel(padding=0.3)
    assert panel.width >= 2.0
    assert panel.height >= 1.5
