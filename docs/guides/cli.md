# Command-Line Interface (CLI) Guide

Animora includes a fast command-line tool `animora` with four core commands.

---

## Commands Reference

### 1. `animora new <filename>`
Scaffold a starter scene with starter components:
```bash
animora new my_scene.py
```

### 2. `animora preview <file> [scene]`
Render a fast, low-quality preview:
```bash
animora preview my_scene.py --open
```

### 3. `animora render <file> [scene]`
Render a high-quality production export:
```bash
# 1080p 60fps
animora render my_scene.py

# 4K resolution
animora render my_scene.py --quality 4k
```

### 4. `animora doctor`
Diagnose Python environment, dependencies, and media tools:
```bash
animora doctor
```
