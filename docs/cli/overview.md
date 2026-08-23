# Animora CLI (Phase 9 Reference)

## 1. Overview

Animora includes a lightweight, fast command-line interface (`animora`) designed to streamline the developer experience of creating, previewing, and rendering animations.

```bash
$ animora --help
usage: animora [-h] [-v] <command> ...

Animora: Declarative educational and algorithmic animation framework.

commands:
  <command>
    new       Scaffold a new Animora scene file from a starter template
    preview   Fast low-quality render for rapid scene iteration
    render    Full production-quality render for final export
    doctor    Diagnose system environment, Python dependencies, and Manim setup
```

---

## 2. Command Reference

### `animora new <filename>`
Scaffolds a new Animora Python scene file pre-populated with standard starter components (`Text`, `Shape`, `Panel`, `use_theme`).

```bash
# Scaffold a starter scene
animora new my_scene.py

# Force overwrite existing file
animora new my_scene.py --force
```

### `animora preview <file> [scene]`
Renders a scene file using Manim's fast low-quality settings (`-ql`), allowing rapid iterative development.

```bash
# Render fast preview of first scene
animora preview my_scene.py

# Preview and immediately open video in default player
animora preview my_scene.py --open
```

### `animora render <file> [scene]`
Renders a scene file using production-quality presets.

```bash
# Production render (high quality 1080p, 60fps)
animora render my_scene.py

# 4K production render
animora render my_scene.py --quality 4k -p
```

### `animora doctor`
Inspects your Python environment, Animora installation, Manim version, NumPy, NetworkX, and system binaries (FFmpeg).

```bash
$ animora doctor
============================================================
 Animora System & Environment Diagnostics
============================================================
[PASS]   Python       : Python 3.11.8 (>= 3.10 supported)
[PASS]   Animora      : Animora 0.1.0.dev0 installed
[PASS]   Manim        : Manim Community 0.18.1 (compatible)
[PASS]   NumPy        : NumPy 1.26.4 installed
[PASS]   NetworkX     : NetworkX 3.2.1 installed
[PASS]   FFmpeg       : FFmpeg binary found at /usr/bin/ffmpeg
============================================================
Status: Environment is fully ready for Animora visualizations.
```
