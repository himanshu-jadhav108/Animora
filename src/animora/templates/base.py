"""Base abstractions and layout scaffolding for Animora scene templates."""

from __future__ import annotations

from typing import Any

import manim

from animora.components.label import Label
from animora.components.panel import Panel
from animora.components.text import Text
from animora.core.camera import MovingCameraScene
from animora.theme.builtin import ModernDark
from animora.theme.context import get_active_theme, use_theme
from animora.theme.theme import Theme


class BaseTemplateScene(MovingCameraScene):
    """Foundational base scene providing standard presentation regions.

    Standard regions:
    - Header: Top-aligned title and optional subtitle
    - Stage: Centered canvas for primary visual components
    - Footer / Status: Bottom-aligned narration or status bar
    """

    default_theme: type[Theme] | Theme = ModernDark

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.title_label: Label | None = None
        self.status_panel: Panel | None = None
        self.status_text: Text | None = None

    def construct(self) -> None:
        """Entrypoint executing construct_template inside active theme scope."""
        with use_theme(self.default_theme):
            self.construct_template()

    def construct_template(self) -> None:
        """Override in template subclasses to build the specific animation."""
        pass

    def setup_header(
        self,
        title: str,
        subtitle: str | None = None,
        run_time: float = 0.6,
    ) -> None:
        """Create and animate standard educational header banner."""
        active_theme = get_active_theme()
        full_title = f"{title}\n{subtitle}" if subtitle else title
        self.title_label = Label(
            text=full_title,
            font_size=active_theme.typography.font_size_md,
            color=active_theme.colors.primary,
        )
        self.title_label.move_to([0.0, 3.2, 0.0])
        self.play(self.title_label.animate_fade_in(run_time=run_time))

    def setup_footer_narrator(
        self,
        initial_text: str = "",
        run_time: float = 0.5,
    ) -> None:
        """Create a bottom-anchored narration panel for step-by-step narration."""
        active_theme = get_active_theme()
        self.status_text = Text(
            initial_text,
            font_size=active_theme.typography.font_size_sm,
            color=active_theme.colors.text,
        )
        self.status_panel = Panel(
            content=self.status_text,
            width=11.0,
            height=0.8,
            fill_color=active_theme.colors.surface,
            stroke_color=active_theme.colors.border,
        )
        self.status_panel.move_to([0.0, -3.2, 0.0])
        self.play(self.status_panel.animate_create(run_time=run_time))

    def narrate(self, text: str, run_time: float = 0.4) -> None:
        """Update the footer narration panel with new explanation text."""
        if self.status_text is None:
            return
        active_theme = get_active_theme()
        new_text = Text(
            text,
            font_size=active_theme.typography.font_size_sm,
            color=active_theme.colors.text,
        )
        new_text.move_to(self.status_panel.center if self.status_panel else [0.0, -3.2, 0.0])
        self.play(
            manim.Transform(self.status_text.manim_object, new_text.manim_object),
            run_time=run_time,
        )
