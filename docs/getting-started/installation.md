# Installation Guide

## Prerequisites

Animora requires:
- **Python >= 3.10**
- **Manim Community >= 0.18.0**
- **FFmpeg** (system media tool used by Manim for video rendering)

---

## Installing Animora

### Standard Installation
```bash
pip install animora
```

### From Source (Development Mode)
```bash
git clone https://github.com/himanshu-jadhav108/Animora.git
cd Animora
pip install -e ".[dev]"
```

---

## Environment Verification with `animora doctor`

Run Animora's built-in diagnostic tool to verify all system binaries and dependencies:

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
