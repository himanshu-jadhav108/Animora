"""Handler for 'animora new <filename>' command."""

from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_TEMPLATE = '''"""Starter Animora scene."""

from __future__ import annotations

from animora.core import Scene
from animora.components import Text, Shape, Panel
from animora.theme import ModernDark, use_theme


class StarterScene(Scene):
    """A minimal starter scene created by 'animora new'."""

    def construct(self) -> None:
        with use_theme(ModernDark):
            title = Text("Welcome to Animora!", font_size=40)
            title.move_to([0, 2.5, 0])

            circle = Shape.circle(radius=0.7)
            card = Panel(circle, title="Visual Primitive")

            self.play(title.animate_fade_in(run_time=0.8))
            self.play(card.animate_create(run_time=1.0))
            self.play(circle.animate_highlight(run_time=0.8))
            self.wait(1)
'''


def register_new_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register 'new' subcommand arguments."""
    parser = subparsers.add_parser(
        "new",
        help="Scaffold a new Animora scene file from a starter template",
        description="Create a well-commented starter scene demonstrating basic Animora components.",
    )
    parser.add_argument(
        "filename",
        type=str,
        help="Path or name of the python file to create (e.g. my_scene.py)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite target file if it already exists",
    )
    parser.set_defaults(func=handle_new)


def handle_new(args: argparse.Namespace) -> int:
    """Execute 'new' command."""
    target_path = Path(args.filename)
    if not target_path.suffix:
        target_path = target_path.with_suffix(".py")

    if target_path.exists() and not args.force:
        print(f"Error: File '{target_path}' already exists. Use --force to overwrite.")
        return 1

    template_file = Path(__file__).parent / "templates" / "basic_scene.py.template"
    if template_file.exists():
        content = template_file.read_text(encoding="utf-8")
    else:
        content = DEFAULT_TEMPLATE

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")

    print(f"Created Animora starter scene at '{target_path}'.")
    print(f"Run 'animora preview {target_path}' to render a fast preview.")
    return 0


__all__ = [
    "handle_new",
    "register_new_parser",
]
