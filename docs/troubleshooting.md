# Troubleshooting & Diagnostics

Common issues, error messages, and resolution steps when developing with Animora.

---

## 1. Run Diagnostics

Whenever an unexpected environment issue arises, start with:

```bash
animora doctor
```

---

## 2. Common Issues & Solutions

### `FFmpeg binary not found`
- **Cause**: Manim requires FFmpeg to encode output MP4/GIF videos.
- **Fix**:
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu/Debian**: `sudo apt install ffmpeg`
  - **Windows**: Install via `winget install Gyan.FFmpeg` or download from [ffmpeg.org](https://ffmpeg.org).

### `LaTeX / dvisvgm not found`
- **Note**: LaTeX is optional in Animora. Standard `Text` uses system fonts and Cairo rendering.
- **Fix**: If using raw LaTeX formulas in Manim, install a TeX distribution (e.g. MiKTeX, MacTeX, or TeXLive).

### `File already exists` when running `animora new`
- **Fix**: Use `--force` flag to overwrite: `animora new my_scene.py --force`.

### `No Scene class found in file`
- **Fix**: Ensure your scene class inherits from `animora.core.Scene` (or `manim.Scene`) and defines a `def construct(self):` method.
