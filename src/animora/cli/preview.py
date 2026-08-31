"""Handler for 'animora preview <file> [scene]' command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any


def build_preview_command(
    filename: str,
    scene_name: str | None = None,
    open_file: bool = False,
    extra_flags: list[str] | None = None,
) -> list[str]:
    """Construct the Manim command-line argument list for fast low-quality preview."""
    cmd = [sys.executable, "-m", "manim", "-ql"]
    if open_file:
        cmd.append("-p")
    if extra_flags:
        cmd.extend(extra_flags)
    cmd.append(str(filename))
    if scene_name:
        cmd.append(str(scene_name))
    return cmd


def register_preview_parser(subparsers: argparse._SubParsersAction[Any]) -> None:
    """Register 'preview' subcommand arguments."""
    parser = subparsers.add_parser(
        "preview",
        help="Fast low-quality render for rapid scene iteration",
        description="Renders a scene file using low quality settings (-ql) for rapid prototyping.",
    )
    parser.add_argument(
        "file",
        type=str,
        help="Python file containing the Animora scene",
    )
    parser.add_argument(
        "scene",
        nargs="?",
        default=None,
        help="Optional name of the Scene class to render",
    )
    parser.add_argument(
        "-p",
        "--open",
        action="store_true",
        help="Automatically open the rendered video in system media player",
    )
    parser.set_defaults(func=handle_preview)


def handle_preview(args: argparse.Namespace) -> int:
    """Execute 'preview' command."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: Scene file '{file_path}' not found.")
        return 1

    cmd = build_preview_command(
        filename=str(file_path),
        scene_name=args.scene,
        open_file=args.open,
    )

    print(f"Rendering preview for '{file_path}' (low quality, fast)...")
    try:
        res = subprocess.run(cmd)
        return res.returncode
    except Exception as exc:
        print(f"Error during preview rendering: {exc}")
        return 1


__all__ = [
    "build_preview_command",
    "handle_preview",
    "register_preview_parser",
]
