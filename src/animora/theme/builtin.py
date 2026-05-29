"""Built-in themes for Animora."""

from __future__ import annotations

from animora.theme.theme import (
    AnimationTiming,
    ColorPalette,
    CornerRadius,
    SpacingScale,
    StrokeScale,
    Theme,
    Typography,
)

# -----------------------------------------------------------------------------
# 1. Modern Dark (Default)
# -----------------------------------------------------------------------------
ModernDark = Theme(
    name="modern_dark",
    colors=ColorPalette(
        primary="#38BDF8",       # Sky 400
        secondary="#818CF8",     # Indigo 400
        accent="#F59E0B",        # Amber 500
        background="#0F172A",    # Slate 900
        surface="#1E293B",       # Slate 800
        text="#F8FAFC",          # Slate 50
        text_muted="#94A3B8",    # Slate 400
        border="#334155",        # Slate 700
        success="#10B981",       # Emerald 500
        warning="#F59E0B",       # Amber 500
        error="#EF4444",         # Red 500
    ),
    typography=Typography(
        font_family=None,
        font_size_xs=18.0,
        font_size_sm=24.0,
        font_size_md=32.0,
        font_size_lg=40.0,
        font_size_xl=48.0,
        line_spacing=1.0,
    ),
    spacing=SpacingScale(xs=0.1, sm=0.25, md=0.5, lg=1.0, xl=2.0),
    strokes=StrokeScale(thin=1.0, regular=2.5, thick=4.0),
    corner_radius=CornerRadius(none=0.0, sm=0.1, md=0.2, lg=0.4, full=0.8),
    timing=AnimationTiming(fast=0.4, normal=1.0, slow=2.0),
)

# -----------------------------------------------------------------------------
# 2. Paper Light
# -----------------------------------------------------------------------------
PaperLight = Theme(
    name="paper_light",
    colors=ColorPalette(
        primary="#2563EB",       # Blue 600
        secondary="#7C3AED",     # Violet 600
        accent="#D97706",        # Amber 600
        background="#FFFFFF",    # White
        surface="#F8FAFC",       # Slate 50
        text="#0F172A",          # Slate 900
        text_muted="#64748B",    # Slate 500
        border="#E2E8F0",        # Slate 200
        success="#059669",       # Emerald 600
        warning="#D97706",       # Amber 600
        error="#DC2626",         # Red 600
    ),
    typography=Typography(
        font_family=None,
        font_size_xs=18.0,
        font_size_sm=24.0,
        font_size_md=32.0,
        font_size_lg=40.0,
        font_size_xl=48.0,
        line_spacing=1.0,
    ),
    spacing=SpacingScale(xs=0.1, sm=0.25, md=0.5, lg=1.0, xl=2.0),
    strokes=StrokeScale(thin=1.0, regular=2.5, thick=4.0),
    corner_radius=CornerRadius(none=0.0, sm=0.1, md=0.2, lg=0.4, full=0.8),
    timing=AnimationTiming(fast=0.4, normal=1.0, slow=2.0),
)

# -----------------------------------------------------------------------------
# 3. Cyberpunk (Neon High-Contrast)
# -----------------------------------------------------------------------------
Cyberpunk = Theme(
    name="cyberpunk",
    colors=ColorPalette(
        primary="#EC4899",       # Pink 500
        secondary="#00F0FF",     # Cyan Neon
        accent="#10B981",        # Emerald
        background="#0A0A0F",    # Deep Void
        surface="#1A102F",       # Synth Dark
        text="#FFFFFF",          # Pure White
        text_muted="#A78BFA",    # Purple 400
        border="#EC4899",        # Neon Pink border
        success="#10B981",
        warning="#FBBF24",
        error="#F43F5E",
    ),
    typography=Typography(
        font_family=None,
        font_size_xs=18.0,
        font_size_sm=24.0,
        font_size_md=32.0,
        font_size_lg=40.0,
        font_size_xl=48.0,
        line_spacing=1.0,
    ),
    spacing=SpacingScale(xs=0.1, sm=0.25, md=0.5, lg=1.0, xl=2.0),
    strokes=StrokeScale(thin=1.5, regular=3.0, thick=5.0),
    corner_radius=CornerRadius(none=0.0, sm=0.0, md=0.1, lg=0.2, full=0.4),
    timing=AnimationTiming(fast=0.3, normal=0.8, slow=1.8),
)

# -----------------------------------------------------------------------------
# 4. Monokai (Code Editor Palette)
# -----------------------------------------------------------------------------
Monokai = Theme(
    name="monokai",
    colors=ColorPalette(
        primary="#A6E22E",       # Monokai Green
        secondary="#66D9EF",     # Monokai Cyan
        accent="#F92672",        # Monokai Magenta
        background="#272822",    # Monokai Charcoal
        surface="#3E3D32",       # Monokai Surface
        text="#F8F8F2",          # Monokai White
        text_muted="#75715E",    # Monokai Comment Gray
        border="#49483E",        # Monokai Border
        success="#A6E22E",
        warning="#FD971F",
        error="#F92672",
    ),
    typography=Typography(
        font_family=None,
        font_size_xs=18.0,
        font_size_sm=24.0,
        font_size_md=32.0,
        font_size_lg=40.0,
        font_size_xl=48.0,
        line_spacing=1.0,
    ),
    spacing=SpacingScale(xs=0.1, sm=0.25, md=0.5, lg=1.0, xl=2.0),
    strokes=StrokeScale(thin=1.0, regular=2.5, thick=4.0),
    corner_radius=CornerRadius(none=0.0, sm=0.1, md=0.2, lg=0.3, full=0.6),
    timing=AnimationTiming(fast=0.4, normal=1.0, slow=2.0),
)

# Default alias
DefaultTheme = ModernDark

__all__ = [
    "Cyberpunk",
    "DefaultTheme",
    "ModernDark",
    "Monokai",
    "PaperLight",
]
