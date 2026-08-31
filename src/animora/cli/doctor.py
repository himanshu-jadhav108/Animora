"""Handler for 'animora doctor' environment diagnostic command."""

from __future__ import annotations

import argparse
import shutil
import sys
from typing import Any, NamedTuple


class DiagnosticResult(NamedTuple):
    name: str
    status: str  # "PASS", "WARN", "FAIL"
    message: str
    advice: str | None = None


def check_environment() -> list[DiagnosticResult]:
    """Inspect local system and python environment for Animora compatibility."""
    results: list[DiagnosticResult] = []

    # 1. Python Version (>=3.10)
    py_ver = sys.version_info
    py_str = f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"
    if py_ver >= (3, 10):
        results.append(DiagnosticResult("Python", "PASS", f"Python {py_str} (>= 3.10 supported)"))
    else:
        results.append(
            DiagnosticResult(
                "Python",
                "FAIL",
                f"Python {py_str} (< 3.10 unsupported)",
                "Upgrade Python to 3.10 or higher.",
            )
        )

    # 2. Animora Version
    try:
        import animora

        results.append(
            DiagnosticResult("Animora", "PASS", f"Animora {animora.__version__} installed")
        )
    except ImportError:
        results.append(
            DiagnosticResult("Animora", "FAIL", "Animora package not found in Python path")
        )

    # 3. Manim Version (>=0.18.0)
    try:
        import manim

        manim_ver = getattr(manim, "__version__", "unknown")
        # Check minimum version 0.18
        if manim_ver != "unknown" and tuple(
            int(x) for x in manim_ver.split(".")[:2] if x.isdigit()
        ) >= (0, 18):
            results.append(
                DiagnosticResult("Manim", "PASS", f"Manim Community {manim_ver} (compatible)")
            )
        else:
            results.append(
                DiagnosticResult(
                    "Manim",
                    "WARN",
                    f"Manim Community {manim_ver} (recommended >= 0.18.0)",
                    "Run 'pip install --upgrade manim' to install the recommended version.",
                )
            )
    except ImportError:
        results.append(
            DiagnosticResult(
                "Manim",
                "FAIL",
                "Manim is not installed",
                "Run 'pip install manim' to install the core graphics backend.",
            )
        )

    # 4. NumPy Version
    try:
        import numpy as np

        results.append(DiagnosticResult("NumPy", "PASS", f"NumPy {np.__version__} installed"))
    except ImportError:
        results.append(DiagnosticResult("NumPy", "FAIL", "NumPy is not installed"))

    # 5. NetworkX Version
    try:
        import networkx as nx

        results.append(DiagnosticResult("NetworkX", "PASS", f"NetworkX {nx.__version__} installed"))
    except ImportError:
        results.append(DiagnosticResult("NetworkX", "FAIL", "NetworkX is not installed"))

    # 6. FFmpeg Binary (Required by Manim)
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        results.append(DiagnosticResult("FFmpeg", "PASS", f"FFmpeg binary found at {ffmpeg_path}"))
    else:
        results.append(
            DiagnosticResult(
                "FFmpeg",
                "WARN",
                "FFmpeg executable not found in system PATH",
                "Install FFmpeg to enable video export in Manim.",
            )
        )

    return results


def register_doctor_parser(subparsers: argparse._SubParsersAction[Any]) -> None:
    """Register 'doctor' subcommand arguments."""
    parser = subparsers.add_parser(
        "doctor",
        help="Diagnose system environment, Python dependencies, and Manim setup",
        description="Inspects Python, Manim, and system dependencies for compatibility.",
    )
    parser.set_defaults(func=handle_doctor)


def handle_doctor(args: argparse.Namespace) -> int:
    """Execute 'doctor' command."""
    print("=" * 60)
    print(" Animora System & Environment Diagnostics")
    print("=" * 60)

    results = check_environment()
    has_failure = False

    for item in results:
        badge = f"[{item.status}]"
        print(f"{badge:<8} {item.name:<12} : {item.message}")
        if item.advice:
            print(f"         └── Advice: {item.advice}")
        if item.status == "FAIL":
            has_failure = True

    print("=" * 60)
    if has_failure:
        print("Status: Issues detected. Please review the failures above.")
        return 1
    else:
        print("Status: Environment is fully ready for Animora visualizations.")
        return 0


__all__ = [
    "DiagnosticResult",
    "check_environment",
    "handle_doctor",
    "register_doctor_parser",
]
