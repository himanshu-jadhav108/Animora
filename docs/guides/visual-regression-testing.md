# Visual Regression Testing Guide

Animora includes an automated visual regression testing subsystem located in `tests/visual_regression/`.
This system renders representative frames from key visual components using Manim's CPU Cairo renderer, compares the rendered frames against committed reference baselines, and flags unintended visual drift or layout regressions.

---

## 🎯 What It Tests

While unit tests verify Python data models (`ArrayListModel`, `BSTModel`, etc.) and integration tests verify that scenes render without raising runtime exceptions (`dry_run=True`), visual regression testing tests the **actual rendered frame output**:
- Shape geometry and stroke rendering
- Node positioning, spacing, and layout calculations
- Semantic highlight styles and accent colors
- Animation transition outcomes (e.g. swap, node insertion, cell highlight)

Current covered components:
- **`Array`**: construction and `animate_swap` result
- **`Table`**: construction and `animate_highlight_cell` result
- **`BST`**: tree layout and `animate_insert` result
- **`TensorGrid`**: matrix layout and `animate_highlight_cell` result
- **`BarChart`**: axes, bars, and `animate_highlight_bar` result
- **`LineChart`**: coordinate path and `animate_draw` result

---

## ⚙️ How It Works

1. **Deterministic Cairo Rendering**: Each test scene runs in a dedicated Manim context configured with `renderer="cairo"` at `640x360` resolution with video output disabled (`write_to_movie=False`). Frame capture is performed directly from the camera buffer.
2. **Settled State Capture**: Each test scene calls `self.wait(0.1)` at the end of its construction to guarantee that all animation transforms have settled into a deterministic final frame.
3. **Subpixel & Anti-Aliasing Tolerance**: Per-channel color differences below `pixel_tolerance = 12.0` are classified as matching, accommodating subtle antialiasing and rasterization boundaries.
4. **Mismatch Ratio Threshold**: If the fraction of mismatched pixels exceeds `max_mismatch_ratio = 0.005` (0.5%), the test fails with a visual regression error.

---

## 🚀 Running Locally

To run all visual regression tests:
```bash
pytest tests/visual_regression/ -v
```

To run visual regression tests using the pytest marker:
```bash
pytest -m "visual_regression" -v
```

To exclude visual regression tests during fast local iteration:
```bash
pytest -m "not visual_regression"
```

---

## 🔍 Inspecting Failures

When a visual regression test detects mismatch beyond the allowable threshold:
1. The test raises an `AssertionError` reporting the exact mismatch percentage and file paths.
2. Two diagnostic images are saved to `tests/visual_regression/failures/`:
   - `{test_id}_actual.png`: The newly rendered frame produced by your code.
   - `{test_id}_diff.png`: A visual diff overlay where matching pixels are dimmed and differing pixels are highlighted in bright magenta (`#FF00B4`).
3. You can inspect these images side-by-side with the reference baseline in `tests/visual_regression/baselines/{test_id}.png`.

---

## 🔄 Intentionally Updating Baselines

When you intentionally change styling, theme colors, layout spacing, or component geometry, the baselines must be updated to reflect the new intended visual design.

### Method 1: Pytest CLI Flag
Update all baselines:
```bash
pytest tests/visual_regression/ --update-baselines
```

Update a single test's baseline:
```bash
pytest tests/visual_regression/ --update-baselines -k test_visual_array
```

### Method 2: Environment Variable
```bash
ANIMORA_UPDATE_BASELINES=1 pytest tests/visual_regression/
```

Always visually inspect the updated images in `tests/visual_regression/baselines/` before committing to ensure the new baseline represents the intended visual design.

---

## ☁️ Continuous Integration (CI)

In GitHub Actions (`.github/workflows/ci.yml`), visual regression tests run in a dedicated job on **Ubuntu with Python 3.12**:
- Linux provides deterministic font rendering and package dependencies (`libcairo2-dev`, `libpango1.0-dev`).
- Cross-OS font differences (e.g. between Windows DirectWrite, macOS CoreText, and Linux FreeType) would otherwise require artificially wide tolerances that defeat regression sensitivity.
- If a pull request triggers a visual regression failure on CI, the failure artifacts (`_actual.png` and `_diff.png`) are automatically uploaded as a downloadable GitHub Actions artifact (`visual-regression-failures`).
