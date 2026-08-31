"""Unit tests for 'animora doctor' command."""

from __future__ import annotations

from animora.cli.doctor import check_environment
from animora.cli.main import create_parser


def test_doctor_diagnostics_structure() -> None:
    """Verify check_environment returns expected diagnostic items."""
    results = check_environment()
    names = [r.name for r in results]

    assert "Python" in names
    assert "Animora" in names
    assert "Manim" in names
    assert "NumPy" in names
    assert "NetworkX" in names

    # Status must be PASS, WARN, or FAIL
    for r in results:
        assert r.status in ("PASS", "WARN", "FAIL")


def test_doctor_cli_dispatch() -> None:
    """Verify doctor command dispatches cleanly through parser."""
    parser = create_parser()
    args = parser.parse_args(["doctor"])
    ret = args.func(args)
    assert ret in (0, 1)
