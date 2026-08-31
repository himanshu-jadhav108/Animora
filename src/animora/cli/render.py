"""Handler for 'animora render <file> [scene]' command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any


def build_render_command(
    filename: str,
    scene_name: str | None = None,
    quality: str = "high",
    open_file: bool = False,
) -> list[str]:
    """Construct the Manim command-line argument list for production render."""
    quality_flag_map = {
        "low": "-ql",
        "medium": "-qm",
        "high": "-qh",
        "4k": "-qk",
    }
    q_flag = quality_flag_map.get(quality.lower(), "-qh")

    cmd = [sys.executable, "-m", "manim", q_flag]
    if open_file:
        cmd.append("-p")
    cmd.append(str(filename))
    if scene_name:
        cmd.append(str(scene_name))
    return cmd


def register_render_parser(subparsers: argparse._SubParsersAction[Any]) -> None:
    """Register 'render' subcommand arguments."""
    parser = subparsers.add_parser(
        "render",
        help="Full production-quality render for final export",
        description="Renders a scene file using production-quality settings.",
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
        "-q",
        "--quality",
        choices=["low", "medium", "high", "4k"],
        default="high",
        help="Render quality preset (default: high)",
    )
    parser.add_argument(
        "-p",
        "--open",
        action="store_true",
        help="Automatically open the rendered video upon completion",
    )
    parser.set_defaults(func=handle_render)


def handle_render(args: argparse.Namespace) -> int:
    """Execute 'render' command."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: Scene file '{file_path}' not found.")
        return 1

    cmd = build_render_command(
        filename=str(file_path),
        scene_name=args.scene,
        quality=args.quality,
        open_file=args.open,
    )

    print(f"Rendering '{file_path}' (quality: {args.quality})...")
    try:
        res = subprocess.run(cmd)
        return res.returncode
    except Exception as exc:
        print(f"Error during production rendering: {exc}")
        return 1


__all__ = [
    "build_render_command",
    "handle_render",
    "register_render_parser",
]
