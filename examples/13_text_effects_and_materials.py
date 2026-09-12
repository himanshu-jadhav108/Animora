"""Example 13: Composable Effects Engine and Stylized Typography.

Demonstrates applying composable visual effects (gradient reveal, glitch, pulse glow)
to Text components parameterized by distinct theme tokens (Aurora, Cyberpunk, ModernDark).
"""

from __future__ import annotations

from animora.components import Text
from animora.core import Scene
from animora.theme import Cyberpunk, ModernDark
from animora.theme.effects import Aurora


class TextEffectsDemoScene(Scene):
    """Visual gallery of composable text effects in pure 2D CPU Cairo."""

    def construct(self) -> None:
        # 1. Gradient Reveal in Aurora Theme
        title = Text("AURORA EFFECTS", font_size=40).move_to([0.0, 1.8, 0.0])
        self.play(title.apply_effect("gradient_reveal", theme=Aurora, run_time=1.2))
        self.wait(0.4)

        # 2. Glitch Effect in Cyberpunk Theme
        glitch_text = Text("CYBERPUNK GLITCH", font_size=34).move_to([0.0, 0.2, 0.0])
        self.play(glitch_text.animate_create())
        self.play(glitch_text.apply_effect("glitch", theme=Cyberpunk, run_time=0.8))
        self.wait(0.4)

        # 3. Pulse Glow in ModernDark Theme
        pulse_text = Text("PULSE EMPHASIS", font_size=30).move_to([0.0, -1.4, 0.0])
        self.play(pulse_text.animate_fade_in())
        self.play(pulse_text.apply_effect("pulse_glow", theme=ModernDark, run_time=0.6))
        self.wait(0.5)


if __name__ == "__main__":
    scene = TextEffectsDemoScene()
    scene.render()
