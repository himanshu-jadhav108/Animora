# Documentation Media Strategy & CI Policy

## 1. Context & Objectives

Animora is an animation framework. Seeing animated visual outputs alongside declarative Python code is essential to demonstrating the library's value proposition within 5 seconds of arriving on the documentation site.

---

## 2. CI Media Strategy: Render-and-Commit vs. Render-in-CI

### Strategy Selected: **Render-and-Commit (Lightweight Vector & GIF Previews)**

| Strategy | Pros | Cons | Verdict |
|---|---|---|---|
| **Render on Every CI Build** | Always in sync with latest code | Extremely slow (3–5 minutes per build), requires full FFmpeg/LaTeX toolchain in docs CI, flaky on cache misses | ❌ Rejected for Normal CI |
| **Render-and-Commit (Selected)** | Instantaneous docs builds ($<15\text{s}$), zero FFmpeg dependency for MkDocs deployment, 100% reliable GitHub Pages builds | Media assets must be refreshed via script when visual examples change | ✅ **Adopted Standard** |

---

## 3. "Docs Preview Quality" Standard

When rendering animated media for documentation embedding via `scripts/render_docs_media.py`:

- **Resolution**: $854 \times 480$ (480p) or responsive SVGs for vector crispness.
- **Framerate**: 30 fps (smooth motion with minimal payload).
- **Duration**: 2 to 4 seconds loop.
- **Format**: Optimized SVG vector animations / lightweight WebM / MP4 / GIF ($< 150\text{ KB}$ per asset).

---

## 4. Script Automation

The entire asset pipeline is managed by `scripts/render_docs_media.py`:

```bash
# Verify all media assets exist without broken links
python scripts/render_docs_media.py --check

# Regenerate all example media assets
python scripts/render_docs_media.py --render
```
