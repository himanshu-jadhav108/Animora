"""Example 03: Theming and Design Tokens (ModernDark, PaperLight, Cyberpunk)."""

from __future__ import annotations

from animora.core import Scene
from animora.components import Text, Shape, Panel
from animora.theme import Cyberpunk, PaperLight, use_theme


class ThemesAndStylingScene(Scene):
    """Demonstrates built-in themes and local theme scoping with use_theme()."""

    def construct(self) -> None:
        # 1. Light Theme Component
        with use_theme(PaperLight):
            light_title = Text("Paper Light Theme", font_size=28)
            light_box = Shape.rounded_rectangle(width=3.0, height=1.5)
            light_panel = Panel(light_box, title=light_title).move_to([-3.2, 0, 0])

        # 2. Cyberpunk Neon Theme Component
        with use_theme(Cyberpunk):
            cyber_title = Text("Cyberpunk Neon", font_size=28)
            cyber_box = Shape.rounded_rectangle(width=3.0, height=1.5)
            cyber_panel = Panel(cyber_box, title=cyber_title).move_to([3.2, 0, 0])

        self.play(light_panel.animate_create(run_time=0.8))
        self.play(cyber_panel.animate_create(run_time=0.8))
        self.wait(0.5)


if __name__ == "__main__":
    import manim
    with manim.tempconfig({"quality": "low_quality", "preview": True}):
        scene = ThemesAndStylingScene()
        scene.render()
