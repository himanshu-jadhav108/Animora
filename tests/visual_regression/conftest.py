"""Visual regression testing infrastructure for Animora.

Provides deterministic Cairo-based frame capture, pixel/perceptual comparison with
anti-aliasing tolerance, baseline image management, failure artifact generation,
and CLI/env flags for updating reference baselines.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

import manim
import numpy as np
import pytest
from PIL import Image

BASELINES_DIR = Path(__file__).parent / "baselines"
FAILURES_DIR = Path(__file__).parent / "failures"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add CLI option to update visual regression baseline images."""
    parser.addoption(
        "--update-baselines",
        action="store_true",
        default=False,
        help="Update committed visual regression reference baseline images.",
    )


def render_scene_to_image(
    scene_cls: type[manim.Scene],
    width: int = 640,
    height: int = 360,
) -> Image.Image:
    """Render a scene deterministically using Manim's CPU Cairo renderer to a PIL Image."""
    with manim.tempconfig(
        {
            "renderer": "cairo",
            "pixel_width": width,
            "pixel_height": height,
            "frame_rate": 15,
            "verbosity": "ERROR",
            "write_to_movie": False,
            "disable_caching": True,
        }
    ):
        scene = scene_cls()
        scene.render()
        img = scene.camera.get_image()
        return img.convert("RGBA")


def compare_images(
    actual: Image.Image,
    expected: Image.Image,
    pixel_tolerance: float = 12.0,
    max_mismatch_ratio: float = 0.015,
) -> tuple[bool, float, Image.Image | None]:
    """Compare two PIL images with per-pixel thresholding and mismatch ratio bounds.

    Args:
        actual: Rendered frame from test scene.
        expected: Reference baseline image.
        pixel_tolerance: Max Euclidean/per-channel difference considered matching
            (guards against font rasterization & anti-aliasing differences).
        max_mismatch_ratio: Max fraction of pixels allowed to exceed pixel_tolerance
            (default 1.5%).

    Returns:
        (passed, mismatch_ratio, diff_image)
    """
    act_rgba = np.array(actual.convert("RGBA"), dtype=np.float32)
    exp_rgba = np.array(expected.convert("RGBA"), dtype=np.float32)

    if act_rgba.shape != exp_rgba.shape:
        return False, 1.0, None

    # Calculate color channel difference
    diff = np.abs(act_rgba[:, :, :3] - exp_rgba[:, :, :3])
    max_channel_diff = np.max(diff, axis=-1)

    mismatched_mask = max_channel_diff > pixel_tolerance
    total_pixels = mismatched_mask.size
    mismatch_count = int(np.sum(mismatched_mask))
    mismatch_ratio = mismatch_count / total_pixels

    passed = mismatch_ratio <= max_mismatch_ratio

    # Generate visual diff overlay
    diff_vis = np.zeros_like(act_rgba, dtype=np.uint8)
    diff_vis[:, :, :3] = (act_rgba[:, :, :3] * 0.35).astype(np.uint8)
    diff_vis[:, :, 3] = 255
    # Highlight mismatched pixels in bright magenta
    diff_vis[mismatched_mask] = [255, 0, 180, 255]

    return passed, mismatch_ratio, Image.fromarray(diff_vis, mode="RGBA")


@pytest.fixture
def assert_visual_match(
    request: pytest.FixtureRequest,
) -> Callable[..., None]:
    """Pytest fixture returning assertion function for visual regression tests."""
    update_flag = request.config.getoption("--update-baselines", default=False)
    env_update = os.environ.get("ANIMORA_UPDATE_BASELINES", "0") == "1"
    should_update = update_flag or env_update

    def _assert_match(
        scene_cls: type[manim.Scene],
        test_id: str,
        tolerance: float = 0.015,
        width: int = 640,
        height: int = 360,
    ) -> None:
        actual_img = render_scene_to_image(scene_cls, width=width, height=height)
        BASELINES_DIR.mkdir(parents=True, exist_ok=True)
        baseline_path = BASELINES_DIR / f"{test_id}.png"

        if should_update or not baseline_path.exists():
            actual_img.save(baseline_path, format="PNG")
            return

        expected_img = Image.open(baseline_path).convert("RGBA")
        passed, mismatch_ratio, diff_img = compare_images(
            actual_img,
            expected_img,
            max_mismatch_ratio=tolerance,
        )

        if not passed:
            FAILURES_DIR.mkdir(parents=True, exist_ok=True)
            actual_path = FAILURES_DIR / f"{test_id}_actual.png"
            diff_path = FAILURES_DIR / f"{test_id}_diff.png"
            actual_img.save(actual_path)
            if diff_img is not None:
                diff_img.save(diff_path)

            raise AssertionError(
                f"Visual regression detected in '{test_id}'! "
                f"Mismatch ratio {mismatch_ratio:.3%} exceeds allowed tolerance {tolerance:.3%}. "
                f"Artifacts saved to:\n"
                f"  Actual: {actual_path}\n"
                f"  Diff  : {diff_path}\n"
                f"  Base  : {baseline_path}\n"
                f"To intentionally accept this visual change as new baseline, run:\n"
                f"  pytest --update-baselines -k {test_id}"
            )

    return _assert_match
