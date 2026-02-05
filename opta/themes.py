"""
Terminal Theme System for Opta CLI

Provides curated color themes for terminal output:
- Monokai, Dracula, Nord, Gruvbox (dark themes)
- Solarized Dark/Light, Tomorrow, GitHub (mixed themes)

Usage:
    from opta.themes import get_theme, list_themes, BUILTIN_THEMES

    theme = get_theme("monokai")
    available = list_themes()
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


@dataclass(frozen=True)
class ThemeConfig:
    """
    Immutable configuration for a terminal color theme.

    All color values should be hex colors (#RRGGBB) or named colors
    supported by Rich (e.g., "red", "blue", "green").
    """

    name: str
    user_input_color: str
    tool_output_color: Optional[str]
    tool_error_color: str
    tool_warning_color: str
    assistant_output_color: str
    completion_menu_color: Optional[str]
    completion_menu_bg_color: Optional[str]
    completion_menu_current_color: Optional[str]
    completion_menu_current_bg_color: Optional[str]
    code_theme: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThemeConfig":
        """Create a ThemeConfig from a dictionary."""
        # Normalize keys (allow both underscores and hyphens)
        normalized = {}
        for key, value in data.items():
            normalized_key = key.replace("-", "_")
            normalized[normalized_key] = value

        return cls(
            name=normalized.get("name", "custom"),
            user_input_color=normalized.get("user_input_color", "#00cc00"),
            tool_output_color=normalized.get("tool_output_color"),
            tool_error_color=normalized.get("tool_error_color", "red"),
            tool_warning_color=normalized.get("tool_warning_color", "#FFA500"),
            assistant_output_color=normalized.get("assistant_output_color", "blue"),
            completion_menu_color=normalized.get("completion_menu_color"),
            completion_menu_bg_color=normalized.get("completion_menu_bg_color"),
            completion_menu_current_color=normalized.get("completion_menu_current_color"),
            completion_menu_current_bg_color=normalized.get("completion_menu_current_bg_color"),
            code_theme=normalized.get("code_theme", "default"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary."""
        return asdict(self)

    def merge(self, overrides: Dict[str, Any]) -> "ThemeConfig":
        """
        Create a new theme with overrides applied.

        Only non-None values in overrides will replace theme values.
        """
        base = self.to_dict()
        for key, value in overrides.items():
            normalized_key = key.replace("-", "_")
            if value is not None and normalized_key in base:
                base[normalized_key] = value
        return ThemeConfig.from_dict(base)


# =============================================================================
# Built-in Theme Definitions
# =============================================================================

BUILTIN_THEMES: Dict[str, ThemeConfig] = {
    # -------------------------------------------------------------------------
    # Dark Themes
    # -------------------------------------------------------------------------
    "monokai": ThemeConfig(
        name="monokai",
        user_input_color="#A6E22E",  # Green
        tool_output_color="#F8F8F2",  # Light gray
        tool_error_color="#F92672",  # Pink/red
        tool_warning_color="#FD971F",  # Orange
        assistant_output_color="#66D9EF",  # Cyan
        completion_menu_color="#F8F8F2",
        completion_menu_bg_color="#272822",
        completion_menu_current_color="#272822",
        completion_menu_current_bg_color="#F92672",
        code_theme="monokai",
    ),
    "dracula": ThemeConfig(
        name="dracula",
        user_input_color="#50FA7B",  # Green
        tool_output_color="#F8F8F2",  # Foreground
        tool_error_color="#FF5555",  # Red
        tool_warning_color="#FFB86C",  # Orange
        assistant_output_color="#8BE9FD",  # Cyan
        completion_menu_color="#F8F8F2",
        completion_menu_bg_color="#282A36",
        completion_menu_current_color="#282A36",
        completion_menu_current_bg_color="#FF79C6",
        code_theme="dracula",
    ),
    "nord": ThemeConfig(
        name="nord",
        user_input_color="#A3BE8C",  # Green (Aurora)
        tool_output_color="#ECEFF4",  # Snow Storm
        tool_error_color="#BF616A",  # Red (Aurora)
        tool_warning_color="#EBCB8B",  # Yellow (Aurora)
        assistant_output_color="#88C0D0",  # Frost cyan
        completion_menu_color="#ECEFF4",
        completion_menu_bg_color="#2E3440",
        completion_menu_current_color="#2E3440",
        completion_menu_current_bg_color="#5E81AC",
        code_theme="nord",
    ),
    "gruvbox-dark": ThemeConfig(
        name="gruvbox-dark",
        user_input_color="#B8BB26",  # Green
        tool_output_color="#EBDBB2",  # Light foreground
        tool_error_color="#FB4934",  # Red
        tool_warning_color="#FABD2F",  # Yellow
        assistant_output_color="#83A598",  # Blue
        completion_menu_color="#EBDBB2",
        completion_menu_bg_color="#282828",
        completion_menu_current_color="#282828",
        completion_menu_current_bg_color="#D79921",
        code_theme="gruvbox-dark",
    ),
    "solarized-dark": ThemeConfig(
        name="solarized-dark",
        user_input_color="#859900",  # Green
        tool_output_color="#93A1A1",  # Base1
        tool_error_color="#DC322F",  # Red
        tool_warning_color="#CB4B16",  # Orange
        assistant_output_color="#268BD2",  # Blue
        completion_menu_color="#93A1A1",
        completion_menu_bg_color="#002B36",
        completion_menu_current_color="#002B36",
        completion_menu_current_bg_color="#2AA198",
        code_theme="solarized-dark",
    ),
    # -------------------------------------------------------------------------
    # Light Themes
    # -------------------------------------------------------------------------
    "solarized-light": ThemeConfig(
        name="solarized-light",
        user_input_color="#859900",  # Green
        tool_output_color="#586E75",  # Base01
        tool_error_color="#DC322F",  # Red
        tool_warning_color="#CB4B16",  # Orange
        assistant_output_color="#268BD2",  # Blue
        completion_menu_color="#586E75",
        completion_menu_bg_color="#FDF6E3",
        completion_menu_current_color="#FDF6E3",
        completion_menu_current_bg_color="#2AA198",
        code_theme="solarized-light",
    ),
    "gruvbox-light": ThemeConfig(
        name="gruvbox-light",
        user_input_color="#79740E",  # Green
        tool_output_color="#3C3836",  # Dark foreground
        tool_error_color="#9D0006",  # Red
        tool_warning_color="#B57614",  # Yellow
        assistant_output_color="#076678",  # Blue
        completion_menu_color="#3C3836",
        completion_menu_bg_color="#FBF1C7",
        completion_menu_current_color="#FBF1C7",
        completion_menu_current_bg_color="#D79921",
        code_theme="gruvbox-light",
    ),
    "github": ThemeConfig(
        name="github",
        user_input_color="#22863A",  # Green
        tool_output_color="#24292E",  # Gray dark
        tool_error_color="#D73A49",  # Red
        tool_warning_color="#E36209",  # Orange
        assistant_output_color="#005CC5",  # Blue
        completion_menu_color="#24292E",
        completion_menu_bg_color="#FFFFFF",
        completion_menu_current_color="#FFFFFF",
        completion_menu_current_bg_color="#0366D6",
        code_theme="github-dark",
    ),
    # -------------------------------------------------------------------------
    # Default Theme (minimal styling)
    # -------------------------------------------------------------------------
    "default": ThemeConfig(
        name="default",
        user_input_color="green",
        tool_output_color=None,
        tool_error_color="red",
        tool_warning_color="#FFA500",
        assistant_output_color="blue",
        completion_menu_color=None,
        completion_menu_bg_color=None,
        completion_menu_current_color=None,
        completion_menu_current_bg_color=None,
        code_theme="default",
    ),
}

# Theme aliases for convenience
THEME_ALIASES: Dict[str, str] = {
    "gruvbox": "gruvbox-dark",
    "solarized": "solarized-dark",
    "tomorrow": "github",  # Similar light theme
    "tomorrow-night": "dracula",  # Similar dark theme
}


def get_theme(name: str) -> Optional[ThemeConfig]:
    """
    Get a theme by name.

    Args:
        name: Theme name (case-insensitive)

    Returns:
        ThemeConfig if found, None otherwise
    """
    name_lower = name.lower()

    # Check aliases first
    if name_lower in THEME_ALIASES:
        name_lower = THEME_ALIASES[name_lower]

    return BUILTIN_THEMES.get(name_lower)


def list_themes() -> list[str]:
    """
    List all available theme names.

    Returns:
        Sorted list of theme names (including aliases)
    """
    themes = set(BUILTIN_THEMES.keys())
    themes.update(THEME_ALIASES.keys())
    return sorted(themes)


def load_theme_file(path: Path) -> ThemeConfig:
    """
    Load a theme from a YAML file.

    Args:
        path: Path to the theme YAML file

    Returns:
        ThemeConfig loaded from file

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is invalid
    """
    if not path.exists():
        raise FileNotFoundError(f"Theme file not found: {path}")

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError(f"Theme file must be a YAML dictionary: {path}")

        return ThemeConfig.from_dict(data)

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in theme file {path}: {e}")


def format_theme_list() -> str:
    """
    Format a nice list of available themes for CLI output.

    Returns:
        Formatted string with theme names and descriptions
    """
    lines = ["Available themes:", ""]

    # Dark themes
    lines.append("  Dark themes:")
    for name in ["monokai", "dracula", "nord", "gruvbox-dark", "solarized-dark"]:
        theme = BUILTIN_THEMES[name]
        lines.append(f"    {name:20} - {_get_theme_description(name)}")

    lines.append("")

    # Light themes
    lines.append("  Light themes:")
    for name in ["github", "solarized-light", "gruvbox-light"]:
        theme = BUILTIN_THEMES[name]
        lines.append(f"    {name:20} - {_get_theme_description(name)}")

    lines.append("")

    # Aliases
    lines.append("  Aliases:")
    for alias, target in sorted(THEME_ALIASES.items()):
        lines.append(f"    {alias:20} -> {target}")

    lines.append("")
    lines.append("  Use --theme-file to load a custom theme from a YAML file.")

    return "\n".join(lines)


def _get_theme_description(name: str) -> str:
    """Get a brief description for a theme."""
    descriptions = {
        "monokai": "Classic dark theme with vibrant colors",
        "dracula": "Popular dark theme with purple accents",
        "nord": "Arctic-inspired dark theme",
        "gruvbox-dark": "Retro groove dark theme",
        "gruvbox-light": "Retro groove light theme",
        "solarized-dark": "Precision dark theme by Ethan Schoonover",
        "solarized-light": "Precision light theme by Ethan Schoonover",
        "github": "Clean light theme inspired by GitHub",
        "default": "Minimal default styling",
    }
    return descriptions.get(name, "")
