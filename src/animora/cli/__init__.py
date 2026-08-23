"""Command-line interface for Animora."""

from __future__ import annotations

from animora.cli.doctor import check_environment, handle_doctor
from animora.cli.main import create_parser, main
from animora.cli.new import handle_new
from animora.cli.preview import build_preview_command, handle_preview
from animora.cli.render import build_render_command, handle_render

__all__: list[str] = [
    "build_preview_command",
    "build_render_command",
    "check_environment",
    "create_parser",
    "handle_doctor",
    "handle_new",
    "handle_preview",
    "handle_render",
    "main",
]
