"""Tests for the Opta CLI theme system."""

import tempfile
from pathlib import Path

import pytest
import yaml

from opta.themes import (
    BUILTIN_THEMES,
    THEME_ALIASES,
    ThemeConfig,
    format_theme_list,
    get_theme,
    list_themes,
    load_theme_file,
)
from opta.theme_manager import ThemeManager, get_theme_manager, reset_theme_manager


class TestThemeConfig:
    """Tests for ThemeConfig dataclass."""

    def test_theme_config_immutable(self):
        """ThemeConfig should be immutable (frozen)."""
        theme = get_theme("monokai")
        with pytest.raises(AttributeError):
            theme.name = "changed"

    def test_from_dict_basic(self):
        """Test creating ThemeConfig from dictionary."""
        data = {
            "name": "test",
            "user_input_color": "#00ff00",
            "tool_error_color": "red",
            "tool_warning_color": "#FFA500",
            "assistant_output_color": "blue",
            "code_theme": "monokai",
        }
        theme = ThemeConfig.from_dict(data)
        assert theme.name == "test"
        assert theme.user_input_color == "#00ff00"
        assert theme.tool_output_color is None  # Default

    def test_from_dict_normalizes_hyphens(self):
        """Test that from_dict normalizes hyphens to underscores."""
        data = {
            "name": "test",
            "user-input-color": "#00ff00",
            "tool-error-color": "red",
            "tool-warning-color": "#FFA500",
            "assistant-output-color": "blue",
            "code-theme": "monokai",
        }
        theme = ThemeConfig.from_dict(data)
        assert theme.user_input_color == "#00ff00"
        assert theme.code_theme == "monokai"

    def test_to_dict(self):
        """Test converting ThemeConfig to dictionary."""
        theme = get_theme("monokai")
        data = theme.to_dict()
        assert data["name"] == "monokai"
        assert data["user_input_color"] == "#A6E22E"
        assert "code_theme" in data

    def test_merge_overrides(self):
        """Test merging overrides into a theme."""
        theme = get_theme("monokai")
        merged = theme.merge({"user_input_color": "#ff0000"})
        assert merged.user_input_color == "#ff0000"
        assert merged.name == "monokai"  # Unchanged
        # Original should be unchanged
        assert theme.user_input_color == "#A6E22E"

    def test_merge_ignores_none_values(self):
        """Test that merge ignores None values."""
        theme = get_theme("monokai")
        merged = theme.merge({"user_input_color": None})
        assert merged.user_input_color == "#A6E22E"  # Unchanged

    def test_merge_normalizes_keys(self):
        """Test that merge normalizes hyphenated keys."""
        theme = get_theme("monokai")
        merged = theme.merge({"user-input-color": "#ff0000"})
        assert merged.user_input_color == "#ff0000"


class TestBuiltinThemes:
    """Tests for built-in themes."""

    def test_all_builtin_themes_exist(self):
        """Verify all expected built-in themes exist."""
        expected = [
            "monokai", "dracula", "nord", "gruvbox-dark", "gruvbox-light",
            "solarized-dark", "solarized-light", "github", "default"
        ]
        for name in expected:
            assert name in BUILTIN_THEMES, f"Missing theme: {name}"

    def test_builtin_themes_have_required_fields(self):
        """All built-in themes should have all required fields."""
        required_fields = [
            "name", "user_input_color", "tool_error_color",
            "tool_warning_color", "assistant_output_color", "code_theme"
        ]
        for name, theme in BUILTIN_THEMES.items():
            for field in required_fields:
                value = getattr(theme, field)
                assert value is not None, f"Theme {name} missing {field}"

    def test_dark_themes_have_dark_backgrounds(self):
        """Dark themes should have dark completion menu backgrounds."""
        dark_themes = ["monokai", "dracula", "nord", "gruvbox-dark", "solarized-dark"]
        for name in dark_themes:
            theme = BUILTIN_THEMES[name]
            if theme.completion_menu_bg_color:
                # Dark colors typically start with #2 or #0
                assert theme.completion_menu_bg_color[1] in "0123", \
                    f"Theme {name} may not have dark background"


class TestThemeAliases:
    """Tests for theme aliases."""

    def test_aliases_resolve_correctly(self):
        """Test that aliases resolve to valid themes."""
        for alias, target in THEME_ALIASES.items():
            assert target in BUILTIN_THEMES, f"Alias {alias} -> {target} is invalid"

    def test_get_theme_with_alias(self):
        """Test get_theme works with aliases."""
        assert get_theme("gruvbox") == get_theme("gruvbox-dark")
        assert get_theme("solarized") == get_theme("solarized-dark")
        assert get_theme("tomorrow") == get_theme("github")


class TestGetTheme:
    """Tests for get_theme function."""

    def test_get_theme_by_name(self):
        """Test getting a theme by name."""
        theme = get_theme("monokai")
        assert theme is not None
        assert theme.name == "monokai"

    def test_get_theme_case_insensitive(self):
        """Test that get_theme is case-insensitive."""
        assert get_theme("MONOKAI") == get_theme("monokai")
        assert get_theme("Dracula") == get_theme("dracula")

    def test_get_theme_unknown_returns_none(self):
        """Test that unknown theme returns None."""
        assert get_theme("nonexistent") is None


class TestListThemes:
    """Tests for list_themes function."""

    def test_list_themes_includes_all(self):
        """Test that list_themes includes all themes and aliases."""
        themes = list_themes()
        # Check built-in themes
        for name in BUILTIN_THEMES:
            assert name in themes
        # Check aliases
        for alias in THEME_ALIASES:
            assert alias in themes

    def test_list_themes_sorted(self):
        """Test that list_themes returns sorted list."""
        themes = list_themes()
        assert themes == sorted(themes)


class TestLoadThemeFile:
    """Tests for load_theme_file function."""

    def test_load_theme_file_basic(self):
        """Test loading a theme from YAML file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({
                "name": "custom",
                "user_input_color": "#123456",
                "tool_error_color": "#ff0000",
                "tool_warning_color": "#ffaa00",
                "assistant_output_color": "#0000ff",
                "code_theme": "monokai",
            }, f)
            f.flush()

            theme = load_theme_file(Path(f.name))
            assert theme.name == "custom"
            assert theme.user_input_color == "#123456"

    def test_load_theme_file_not_found(self):
        """Test that missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_theme_file(Path("/nonexistent/theme.yaml"))

    def test_load_theme_file_invalid_yaml(self):
        """Test that invalid YAML raises ValueError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            f.flush()

            with pytest.raises(ValueError, match="Invalid YAML"):
                load_theme_file(Path(f.name))


class TestFormatThemeList:
    """Tests for format_theme_list function."""

    def test_format_theme_list_structure(self):
        """Test that format_theme_list has expected structure."""
        output = format_theme_list()
        assert "Available themes:" in output
        assert "Dark themes:" in output
        assert "Light themes:" in output
        assert "Aliases:" in output
        assert "monokai" in output
        assert "github" in output


class TestThemeManager:
    """Tests for ThemeManager class."""

    def setup_method(self):
        """Reset theme manager before each test."""
        reset_theme_manager()

    def test_resolve_theme_none(self):
        """Test that no arguments returns None."""
        tm = ThemeManager()
        assert tm.resolve_theme() is None

    def test_resolve_theme_dark_mode(self):
        """Test dark mode resolves to monokai."""
        tm = ThemeManager()
        theme = tm.resolve_theme(dark_mode=True)
        assert theme.name == "monokai"

    def test_resolve_theme_light_mode(self):
        """Test light mode resolves to github."""
        tm = ThemeManager()
        theme = tm.resolve_theme(light_mode=True)
        assert theme.name == "github"

    def test_resolve_theme_explicit_name(self):
        """Test explicit theme name."""
        tm = ThemeManager()
        theme = tm.resolve_theme(theme_name="nord")
        assert theme.name == "nord"

    def test_resolve_theme_unknown_raises(self):
        """Test that unknown theme raises ValueError."""
        tm = ThemeManager()
        with pytest.raises(ValueError, match="Unknown theme"):
            tm.resolve_theme(theme_name="nonexistent")

    def test_resolve_theme_conflicting_modes_raises(self):
        """Test that both dark and light mode raises ValueError."""
        tm = ThemeManager()
        with pytest.raises(ValueError, match="Cannot use both"):
            tm.resolve_theme(dark_mode=True, light_mode=True)

    def test_resolve_theme_precedence_theme_over_mode(self):
        """Test that explicit theme takes precedence over mode."""
        tm = ThemeManager()
        # With warnings suppressed
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            theme = tm.resolve_theme(theme_name="nord", dark_mode=True)
        assert theme.name == "nord"

    def test_resolve_theme_with_overrides(self):
        """Test theme with color overrides."""
        tm = ThemeManager()
        theme = tm.resolve_theme(
            theme_name="monokai",
            user_input_color="#ff0000"
        )
        assert theme.user_input_color == "#ff0000"

    def test_resolve_theme_file(self):
        """Test loading theme from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({
                "name": "file_theme",
                "user_input_color": "#abcdef",
                "tool_error_color": "#ff0000",
                "tool_warning_color": "#ffaa00",
                "assistant_output_color": "#0000ff",
                "code_theme": "monokai",
            }, f)
            f.flush()

            tm = ThemeManager()
            theme = tm.resolve_theme(theme_file=f.name)
            assert theme.name == "file_theme"
            assert theme.user_input_color == "#abcdef"

    def test_get_io_colors_none(self):
        """Test get_io_colors with None returns empty dict."""
        tm = ThemeManager()
        assert tm.get_io_colors(None) == {}

    def test_get_io_colors_theme(self):
        """Test get_io_colors extracts all color fields."""
        tm = ThemeManager()
        theme = get_theme("monokai")
        colors = tm.get_io_colors(theme)
        assert colors["user_input_color"] == "#A6E22E"
        assert colors["code_theme"] == "monokai"
        assert len(colors) == 10


class TestGlobalThemeManager:
    """Tests for global theme manager functions."""

    def setup_method(self):
        """Reset theme manager before each test."""
        reset_theme_manager()

    def test_get_theme_manager_singleton(self):
        """Test that get_theme_manager returns singleton."""
        tm1 = get_theme_manager()
        tm2 = get_theme_manager()
        assert tm1 is tm2

    def test_reset_theme_manager(self):
        """Test that reset creates new instance."""
        tm1 = get_theme_manager()
        reset_theme_manager()
        tm2 = get_theme_manager()
        assert tm1 is not tm2
