"""Active theme context management for Animora scenes and components."""

from __future__ import annotations

import contextvars
from collections.abc import Generator
from contextlib import contextmanager

from animora.theme.builtin import DefaultTheme
from animora.theme.theme import Theme

# Context variable holding the currently active theme in execution context
_ACTIVE_THEME: contextvars.ContextVar[Theme] = contextvars.ContextVar(
    "animora_active_theme",
    default=DefaultTheme,
)


def get_active_theme() -> Theme:
    """Retrieve the currently active Theme in the local context."""
    return _ACTIVE_THEME.get()


def set_active_theme(theme: Theme) -> None:
    """Globally or locally set the active theme."""
    _ACTIVE_THEME.set(theme)


@contextmanager
def use_theme(theme: Theme) -> Generator[Theme, None, None]:
    """Context manager for applying a Theme to a block of component creation.

    Example:
    ```python
    with use_theme(PaperLight):
        label = Text("Light Mode")
        box = Shape.rectangle()
    ```
    """
    token = _ACTIVE_THEME.set(theme)
    try:
        yield theme
    finally:
        _ACTIVE_THEME.reset(token)


__all__ = [
    "get_active_theme",
    "set_active_theme",
    "use_theme",
]
