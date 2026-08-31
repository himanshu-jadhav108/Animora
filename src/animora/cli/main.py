"""Main entry point and argument dispatcher for Animora CLI."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

import animora
from animora.cli.doctor import register_doctor_parser
from animora.cli.new import register_new_parser
from animora.cli.preview import register_preview_parser
from animora.cli.render import register_render_parser


def create_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser with all registered subcommands."""
    parser = argparse.ArgumentParser(
        prog="animora",
        description="Animora: Declarative educational and algorithmic animation framework.",
        epilog="Run 'animora <subcommand> --help' for details on specific commands.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"animora {animora.__version__}",
        help="Show Animora version and exit",
    )

    subparsers = parser.add_subparsers(
        dest="subcommand",
        title="commands",
        metavar="<command>",
    )

    # Register exactly 4 approved subcommands
    register_new_parser(subparsers)
    register_preview_parser(subparsers)
    register_render_parser(subparsers)
    register_doctor_parser(subparsers)

    return parser


def main(args: Sequence[str] | None = None) -> int:
    """CLI execution entrypoint."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not hasattr(parsed_args, "func"):
        parser.print_help()
        return 0

    return int(parsed_args.func(parsed_args))


if __name__ == "__main__":
    sys.exit(main())
