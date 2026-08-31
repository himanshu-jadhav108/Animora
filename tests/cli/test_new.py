"""Unit tests for 'animora new' command."""

from __future__ import annotations

import ast
import tempfile
from pathlib import Path

from animora.cli.main import create_parser


def test_animora_new_creates_valid_python_file() -> None:
    """Verify 'animora new' scaffolds a syntactically valid Python file."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_file = Path(tmp_dir) / "test_scene.py"
        parser = create_parser()
        args = parser.parse_args(["new", str(target_file)])
        ret = args.func(args)

        assert ret == 0
        assert target_file.exists()

        content = target_file.read_text(encoding="utf-8")
        # Verify valid AST syntax
        parsed_ast = ast.parse(content)
        assert parsed_ast is not None
        assert "StarterScene" in content
        assert "animora" in content


def test_animora_new_prevents_accidental_overwrite() -> None:
    """Verify 'animora new' fails if file exists without --force."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_file = Path(tmp_dir) / "existing.py"
        target_file.write_text("existing content", encoding="utf-8")

        parser = create_parser()
        args = parser.parse_args(["new", str(target_file)])
        ret = args.func(args)

        assert ret == 1
        assert target_file.read_text(encoding="utf-8") == "existing content"

        # Now test with --force
        args_force = parser.parse_args(["new", str(target_file), "--force"])
        ret_force = args_force.func(args_force)
        assert ret_force == 0
        assert "StarterScene" in target_file.read_text(encoding="utf-8")
