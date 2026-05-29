"""Integration test rendering identical scene under different themes in Manim."""

from __future__ import annotations

import manim
from animora.components.panel import Panel
from animora.components.shape import Shape
from animora.components.text import Text
from animora.core.scene import Scene
from animora.theme.builtin import ModernDark, PaperLight
from animora.theme.context import use_theme


class ThemedScene(Scene):
    """Scene for testing multi-theme rendering."""

    def construct(self) -> None:
        title = Text("Themed Scene Demo", font_size=32)
        circle = Shape.circle(radius=0.5)
        panel = Panel(circle, title="Themed Container")

        self.play(title.animate_fade_in(run_time=0.1))
        self.play(panel.animate_create(run_time=0.1))


def test_themed_rendering_end_to_end() -> None:
    """Verify scene renders cleanly under both ModernDark and PaperLight themes."""
    # 1. Render under ModernDark
    with use_theme(ModernDark):
        with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
            dark_scene = ThemedScene()
            dark_scene.render()
            assert len(dark_scene.mobjects) >= 1

    # 2. Render under PaperLight
    with use_theme(PaperLight):
        with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
            light_scene = ThemedScene()
            light_scene.render()
            assert len(light_scene.mobjects) >= 1
