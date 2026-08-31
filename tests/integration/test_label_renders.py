"""Integration test rendering Label through Animora's Scene end-to-end."""

from __future__ import annotations

import manim

from animora.components.label import Label
from animora.core.scene import Scene


class DemoLabelScene(Scene):
    """Integration scene exercising the full Animora stack."""

    def construct(self) -> None:
        # 1. High-level declarative construction
        label = Label("Hello Animora", font_size=36, color="#38BDF8")
        label.move_to([0, 0, 0])

        # 2. Add and animate with high-level Animora Animation
        self.play(label.animate_fade_in(run_time=0.1))

        # 3. Use escape hatch directly
        label.manim_object.shift(manim.UP * 0.5)

        # 4. Transform text animation
        self.play(label.animate_transform_text("Phase 2 Complete", run_time=0.1))


def test_label_scene_render_end_to_end() -> None:
    """Verify that DemoLabelScene renders through Manim without error in dry_run mode."""
    with manim.tempconfig({"dry_run": True, "verbosity": "WARNING", "write_to_movie": False}):
        scene = DemoLabelScene()
        scene.render()
        assert len(scene.mobjects) >= 1
