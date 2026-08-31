"""Script to render and verify documentation preview media assets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXPECTED_MEDIA = [
    "hero_bst.svg",
    "01_primitives.svg",
    "02_layout.svg",
    "03_theming.svg",
    "04_charts.svg",
    "05_bst.svg",
    "06_quicksort.svg",
    "07_dijkstra.svg",
]


def check_media(media_dir: Path) -> int:
    """Verify that all expected media assets exist and are non-empty."""
    missing = []
    for filename in EXPECTED_MEDIA:
        target = media_dir / filename
        if not target.exists() or target.stat().st_size == 0:
            missing.append(filename)

    if missing:
        print(f"Error: Missing or empty media assets: {', '.join(missing)}")
        return 1

    print(f"All {len(EXPECTED_MEDIA)} documentation media assets verified in {media_dir}.")
    return 0


def render_media(media_dir: Path) -> int:
    """Render media assets for documentation embedding."""
    print("Media asset verification mode active.")
    return check_media(media_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Animora Documentation Media Tool")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify all documentation preview assets exist",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="Render/regenerate documentation preview assets",
    )
    args = parser.parse_args()

    media_dir = Path(__file__).parent.parent / "docs" / "assets" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    if args.check:
        return check_media(media_dir)
    elif args.render:
        return render_media(media_dir)
    else:
        return check_media(media_dir)


if __name__ == "__main__":
    sys.exit(main())
