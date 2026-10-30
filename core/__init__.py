"""
Core package initialization.
"""

from .config import (
    COLOR_BORDER,
    COLOR_CARD_BG,
    COLOR_GRID,
    COLOR_LIGHT_BG,
    COLOR_MUTED_GREY,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    SCENARIO_CONFIGS,
)
from .styles import apply_custom_styles

__all__ = [
    "COLOR_PRIMARY",
    "COLOR_SECONDARY",
    "COLOR_MUTED_GREY",
    "COLOR_LIGHT_BG",
    "COLOR_CARD_BG",
    "COLOR_BORDER",
    "COLOR_GRID",
    "SCENARIO_CONFIGS",
    "apply_custom_styles",
]
