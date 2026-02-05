"""
Theme Manager for Opta CLI

Handles theme resolution, loading, and application.

Usage:
    from opta.theme_manager import ThemeManager

    manager = ThemeManager()
    theme = manager.resolve_theme(
        theme_name="monokai",
        dark_mode=False,
        light_mode=False,
        user_input_color="#00ff00",  # Override
    )
    colors = manager.get_io_colors(theme)
"""

import warnings
from pathlib import Path
from typing import Any, Dict, Optional

from opta.themes import (
    BUILTIN_THEMES,
    ThemeConfig,
    get_theme,
    list_themes,
    load_theme_file,
)


class ThemeManager:
    """
    Manages theme resolution and application.

    Handles:
    - Loading built-in themes
    - Loading custom theme files
    - Resolving theme from args (with precedence rules)
    - Applying color overrides
    - Converting themes to InputOutput kwargs
    """

    def __init__(self):
        self.builtin_themes = BUILTIN_THEMES.copy()
        self.custom_themes: Dict[str, ThemeConfig] = {}

    def load_theme_from_file(self, path: Path) -> ThemeConfig:
        """
        Load a custom theme from a file.

        Args:
            path: Path to the theme YAML file

        Returns:
            The loaded ThemeConfig

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid
        """
        theme = load_theme_file(path)
        self.custom_themes[theme.name] = theme
        return theme

    def resolve_theme(
        self,
        theme_name: Optional[str] = None,
        dark_mode: bool = False,
        light_mode: bool = False,
        theme_file: Optional[str] = None,
        **color_overrides,
    ) -> Optional[ThemeConfig]:
        """
        Resolve the final theme based on arguments.

        Precedence (highest to lowest):
        1. --theme-file (custom file)
        2. --theme NAME (explicit theme)
        3. --dark-mode (alias for monokai)
        4. --light-mode (alias for github)
        5. No theme (returns None, use individual colors)

        Individual color overrides are always applied on top.

        Args:
            theme_name: Explicit theme name (--theme)
            dark_mode: Use dark mode (--dark-mode)
            light_mode: Use light mode (--light-mode)
            theme_file: Path to custom theme file (--theme-file)
            **color_overrides: Individual color overrides

        Returns:
            ThemeConfig with overrides applied, or None if no theme

        Raises:
            ValueError: If theme not found or conflicting args
        """
        # Validate conflicting args
        if dark_mode and light_mode:
            raise ValueError("Cannot use both --dark-mode and --light-mode")

        theme: Optional[ThemeConfig] = None

        # 1. Custom theme file takes highest precedence
        if theme_file:
            theme = self.load_theme_from_file(Path(theme_file))
            if theme_name:
                warnings.warn(
                    f"Both --theme-file and --theme specified. "
                    f"Using --theme-file: {theme_file}"
                )

        # 2. Explicit theme name
        elif theme_name:
            theme = self._get_theme_by_name(theme_name)
            if dark_mode or light_mode:
                mode = "dark" if dark_mode else "light"
                warnings.warn(
                    f"Both --theme={theme_name} and --{mode}-mode specified. "
                    f"Using --theme={theme_name}."
                )

        # 3. Dark mode alias
        elif dark_mode:
            theme = self.builtin_themes["monokai"]

        # 4. Light mode alias
        elif light_mode:
            theme = self.builtin_themes["github"]

        # 5. No theme - return None (caller uses individual colors)
        if theme is None:
            return None

        # Apply color overrides
        overrides = self._filter_color_overrides(color_overrides)
        if overrides:
            theme = theme.merge(overrides)

        return theme

    def _get_theme_by_name(self, name: str) -> ThemeConfig:
        """
        Get a theme by name, checking custom themes first.

        Args:
            name: Theme name

        Returns:
            ThemeConfig

        Raises:
            ValueError: If theme not found
        """
        # Check custom themes first
        if name in self.custom_themes:
            return self.custom_themes[name]

        # Check built-in themes
        theme = get_theme(name)
        if theme is None:
            available = list_themes()
            raise ValueError(
                f"Unknown theme '{name}'. "
                f"Available themes: {', '.join(available)}. "
                f"Use --list-themes to see all themes."
            )

        return theme

    def _filter_color_overrides(self, overrides: Dict[str, Any]) -> Dict[str, Any]:
        """Filter out None values and non-color keys from overrides."""
        color_keys = {
            "user_input_color",
            "tool_output_color",
            "tool_error_color",
            "tool_warning_color",
            "assistant_output_color",
            "completion_menu_color",
            "completion_menu_bg_color",
            "completion_menu_current_color",
            "completion_menu_current_bg_color",
            "code_theme",
        }

        result = {}
        for key, value in overrides.items():
            # Normalize key
            normalized = key.replace("-", "_")
            if normalized in color_keys and value is not None:
                # Check for default values that shouldn't override
                if normalized == "user_input_color" and value == "blue":
                    continue
                if normalized == "tool_error_color" and value == "red":
                    continue
                if normalized == "tool_warning_color" and value == "#FFA500":
                    continue
                if normalized == "assistant_output_color" and value == "blue":
                    continue
                if normalized == "code_theme" and value == "default":
                    continue
                result[normalized] = value

        return result

    def get_io_colors(self, theme: Optional[ThemeConfig]) -> Dict[str, Any]:
        """
        Convert a theme to InputOutput kwargs.

        Args:
            theme: ThemeConfig or None

        Returns:
            Dictionary of kwargs for InputOutput.__init__
        """
        if theme is None:
            return {}

        return {
            "user_input_color": theme.user_input_color,
            "tool_output_color": theme.tool_output_color,
            "tool_error_color": theme.tool_error_color,
            "tool_warning_color": theme.tool_warning_color,
            "assistant_output_color": theme.assistant_output_color,
            "completion_menu_color": theme.completion_menu_color,
            "completion_menu_bg_color": theme.completion_menu_bg_color,
            "completion_menu_current_color": theme.completion_menu_current_color,
            "completion_menu_current_bg_color": theme.completion_menu_current_bg_color,
            "code_theme": theme.code_theme,
        }


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """Get or create the global theme manager."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


def reset_theme_manager():
    """Reset the global theme manager (for testing)."""
    global _theme_manager
    _theme_manager = None
