"""Tokenization model, token-splitting visualizer, and one-call animation API."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import manim
import numpy as np

from animora.components.panel import Panel
from animora.components.text import Text
from animora.core.animation import Animation
from animora.core.config import ComponentConfig
from animora.ml.base import MLComponent, MLTrace
from animora.theme.context import get_active_theme

if TYPE_CHECKING:
    pass


class TokenizerModel:
    """Mathematical rule-based string tokenizer extracting tokens and character offsets."""

    def __init__(self, text: str) -> None:
        self.raw_text = str(text)
        self.tokens: list[str] = []
        self.spans: list[tuple[int, int]] = []
        self.trace = MLTrace()
        self._tokenize()

    def _tokenize(self) -> None:
        # Regex splits alphanumeric sequences and individual punctuation marks
        pattern = re.compile(r"\w+|[^\w\s]")
        for match in pattern.finditer(self.raw_text):
            tok = match.group()
            self.tokens.append(tok)
            self.spans.append((match.start(), match.end()))

        self.trace.record(
            name="tokenization",
            description=f"Extracted {len(self.tokens)} tokens from text.",
            raw_text=self.raw_text,
            tokens=list(self.tokens),
            spans=list(self.spans),
        )


class TokenizerVisualizer(MLComponent):
    """Visualizes splitting raw text into token badges/chips with indices."""

    def __init__(
        self,
        text: str,
        *,
        chip_width: float = 1.3,
        chip_height: float = 0.8,
        spacing: float = 0.25,
        config: ComponentConfig | None = None,
        **kwargs: Any,
    ) -> None:
        self.model = TokenizerModel(text)
        self.chip_width = float(chip_width)
        self.chip_height = float(chip_height)
        self.spacing = float(spacing)
        self.n_tokens = len(self.model.tokens)

        # Compute horizontal positions for token chips
        total_width = (self.n_tokens * self.chip_width) + (max(0, self.n_tokens - 1) * self.spacing)
        self.chip_positions: list[np.ndarray] = []
        start_x = -total_width / 2.0 + (self.chip_width / 2.0)

        for i in range(self.n_tokens):
            x = start_x + (i * (self.chip_width + self.spacing))
            self.chip_positions.append(np.array([x, 0.0, 0.0]))

        super().__init__(config=config, **kwargs)

    def _create_token_chip(self, token: str, idx: int) -> Panel:
        active_theme = get_active_theme()
        body = Text(f"id: {idx}", font_size=11, color=active_theme.colors.text_muted)
        panel = Panel(
            body,
            title=f'"{token}"',
            width=self.chip_width,
            height=self.chip_height,
            padding=0.1,
        )
        return panel

    def _build_mobject(self) -> manim.Mobject:
        group = manim.VGroup()
        for idx, (tok, pos) in enumerate(zip(self.model.tokens, self.chip_positions, strict=False)):
            chip = self._create_token_chip(tok, idx)
            chip.move_to(pos)
            group.add(chip.manim_object)
        return group

    def animate(self) -> list[Animation]:
        """One-call animation showing raw text string resolving into token chips."""
        active_theme = get_active_theme()
        animations: list[Animation] = []

        # 1. Spawn raw string label
        raw_text_mobj = manim.Text(
            f'"{self.model.raw_text}"',
            font_size=20,
            color=active_theme.colors.primary,
        )
        raw_text_mobj.move_to(np.array([0.0, 1.2, 0.0]))

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.Write(raw_text_mobj),
                run_time=0.6,
                name="display_raw_text",
            )
        )

        # 2. Sequential pop-in of individual token chips
        chip_creations = []
        for idx, (tok, pos) in enumerate(zip(self.model.tokens, self.chip_positions, strict=False)):
            chip = self._create_token_chip(tok, idx)
            chip.move_to(pos)
            chip_creations.append(chip.animate_create().to_manim())

        animations.append(
            Animation(
                component=self,
                manim_animation=manim.AnimationGroup(*chip_creations, lag_ratio=0.15),
                run_time=0.8,
                name="spawn_token_chips",
            )
        )

        return animations


def tokenize(text: str) -> list[Animation]:
    """One-call functional API to animate string tokenization into token chips."""
    viz = TokenizerVisualizer(text)
    return viz.animate()


__all__ = [
    "TokenizerModel",
    "TokenizerVisualizer",
    "tokenize",
]
