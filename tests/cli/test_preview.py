"""Unit tests for 'animora preview' command."""

from __future__ import annotations

from animora.cli.preview import build_preview_command


def test_build_preview_command_flags() -> None:
    """Verify preview command constructs low-quality fast render flags."""
    cmd = build_preview_command(
        filename="my_scene.py",
        scene_name="DemoScene",
        open_file=True,
    )

    assert "-m" in cmd
    assert "manim" in cmd
    assert "-ql" in cmd
    assert "-p" in cmd
    assert "my_scene.py" in cmd
    assert "DemoScene" in cmd
