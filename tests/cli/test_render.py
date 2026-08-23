"""Unit tests for 'animora render' command."""

from __future__ import annotations

from animora.cli.render import build_render_command


def test_build_render_command_quality_presets() -> None:
    """Verify render command maps quality presets correctly."""
    cmd_high = build_render_command(filename="scene.py", quality="high")
    assert "-qh" in cmd_high

    cmd_medium = build_render_command(filename="scene.py", quality="medium")
    assert "-qm" in cmd_medium

    cmd_4k = build_render_command(filename="scene.py", quality="4k", open_file=True)
    assert "-qk" in cmd_4k
    assert "-p" in cmd_4k
