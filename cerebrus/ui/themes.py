import winreg

import dearpygui.dearpygui as dpg


class ThemeManager:
    def __init__(self):
        self.themes = {}
        self.current_palette = "Standard"
        self.current_mode = "System"
        self._create_themes()

    def _create_themes(self):
        # Standard Palette
        self._create_theme_variant(
            "Standard",
            "Dark",
            {
                dpg.mvThemeCol_WindowBg: (30, 30, 30),
                dpg.mvThemeCol_ChildBg: (35, 35, 35),
                dpg.mvThemeCol_PopupBg: (40, 40, 40),
                dpg.mvThemeCol_Border: (60, 60, 60),
                dpg.mvThemeCol_FrameBg: (50, 50, 50),
                dpg.mvThemeCol_TitleBg: (40, 40, 40),
                dpg.mvThemeCol_TitleBgActive: (60, 60, 60),
                dpg.mvThemeCol_MenuBarBg: (40, 40, 40),
                dpg.mvThemeCol_Header: (70, 70, 70),
                dpg.mvThemeCol_Button: (60, 60, 60),
                dpg.mvThemeCol_ButtonHovered: (80, 80, 80),
                dpg.mvThemeCol_ButtonActive: (100, 100, 100),
                dpg.mvThemeCol_Text: (220, 220, 220),
            },
        )
        self._create_theme_variant(
            "Standard",
            "Light",
            {
                dpg.mvThemeCol_WindowBg: (240, 240, 240),
                dpg.mvThemeCol_ChildBg: (235, 235, 235),
                dpg.mvThemeCol_PopupBg: (255, 255, 255),
                dpg.mvThemeCol_Border: (180, 180, 180),  # Darker border for visibility
                dpg.mvThemeCol_FrameBg: (255, 255, 255),
                dpg.mvThemeCol_TitleBg: (220, 220, 220),
                dpg.mvThemeCol_TitleBgActive: (200, 200, 200),
                dpg.mvThemeCol_MenuBarBg: (230, 230, 230),
                dpg.mvThemeCol_Header: (200, 200, 200),
                dpg.mvThemeCol_Button: (220, 220, 220),
                dpg.mvThemeCol_ButtonHovered: (200, 200, 200),
                dpg.mvThemeCol_ButtonActive: (180, 180, 180),
                dpg.mvThemeCol_Text: (20, 20, 20),
            },
        )

        # High Contrast Palette
        # Dark: Black background, White/Yellow text, Bright borders
        self._create_theme_variant(
            "High Contrast",
            "Dark",
            {
                dpg.mvThemeCol_WindowBg: (0, 0, 0),
                dpg.mvThemeCol_ChildBg: (0, 0, 0),
                dpg.mvThemeCol_PopupBg: (0, 0, 0),
                dpg.mvThemeCol_Border: (255, 255, 255),  # White border
                dpg.mvThemeCol_FrameBg: (0, 0, 0),
                dpg.mvThemeCol_TitleBg: (0, 0, 0),
                dpg.mvThemeCol_TitleBgActive: (50, 50, 50),
                dpg.mvThemeCol_MenuBarBg: (0, 0, 0),
                dpg.mvThemeCol_Header: (100, 100, 100),
                dpg.mvThemeCol_Button: (0, 0, 0),
                dpg.mvThemeCol_ButtonHovered: (50, 50, 50),
                dpg.mvThemeCol_ButtonActive: (100, 100, 100),
                dpg.mvThemeCol_Text: (255, 255, 255),
            },
        )
        # Light: White background, Black text, Thick Black borders
        self._create_theme_variant(
            "High Contrast",
            "Light",
            {
                dpg.mvThemeCol_WindowBg: (255, 255, 255),
                dpg.mvThemeCol_ChildBg: (255, 255, 255),
                dpg.mvThemeCol_PopupBg: (255, 255, 255),
                dpg.mvThemeCol_Border: (0, 0, 0),  # Black border
                dpg.mvThemeCol_FrameBg: (255, 255, 255),
                dpg.mvThemeCol_TitleBg: (255, 255, 255),
                dpg.mvThemeCol_TitleBgActive: (200, 200, 200),
                dpg.mvThemeCol_MenuBarBg: (255, 255, 255),
                dpg.mvThemeCol_Header: (200, 200, 200),
                dpg.mvThemeCol_Button: (255, 255, 255),
                dpg.mvThemeCol_ButtonHovered: (220, 220, 220),
                dpg.mvThemeCol_ButtonActive: (180, 180, 180),
                dpg.mvThemeCol_Text: (0, 0, 0),
            },
        )

        # Deuteranopia (Green-Blind)
        # Avoids Green/Red confusion. Uses Blue/Yellow/Gray.
        # Dark
        self._create_theme_variant(
            "Deuteranopia",
            "Dark",
            {
                dpg.mvThemeCol_WindowBg: (20, 20, 30),
                dpg.mvThemeCol_ChildBg: (25, 25, 35),
                dpg.mvThemeCol_PopupBg: (30, 30, 40),
                dpg.mvThemeCol_Border: (100, 100, 120),
                dpg.mvThemeCol_FrameBg: (40, 40, 50),
                dpg.mvThemeCol_TitleBg: (30, 30, 40),
                dpg.mvThemeCol_TitleBgActive: (50, 50, 70),
                dpg.mvThemeCol_MenuBarBg: (30, 30, 40),
                dpg.mvThemeCol_Header: (0, 90, 150),  # Blue
                dpg.mvThemeCol_Button: (0, 70, 130),  # Blue
                dpg.mvThemeCol_ButtonHovered: (0, 90, 160),
                dpg.mvThemeCol_ButtonActive: (0, 110, 190),
                dpg.mvThemeCol_Text: (230, 230, 230),
            },
        )
        # Light
        self._create_theme_variant(
            "Deuteranopia",
            "Light",
            {
                dpg.mvThemeCol_WindowBg: (245, 245, 250),
                dpg.mvThemeCol_ChildBg: (240, 240, 245),
                dpg.mvThemeCol_PopupBg: (255, 255, 255),
                dpg.mvThemeCol_Border: (180, 180, 200),
                dpg.mvThemeCol_FrameBg: (255, 255, 255),
                dpg.mvThemeCol_TitleBg: (230, 230, 240),
                dpg.mvThemeCol_TitleBgActive: (210, 210, 230),
                dpg.mvThemeCol_MenuBarBg: (240, 240, 250),
                dpg.mvThemeCol_Header: (100, 180, 255),  # Light Blue
                dpg.mvThemeCol_Button: (220, 230, 255),
                dpg.mvThemeCol_ButtonHovered: (200, 210, 240),
                dpg.mvThemeCol_ButtonActive: (180, 190, 220),
                dpg.mvThemeCol_Text: (10, 10, 30),
            },
        )

        # Tritanopia (Blue-Blind)
        # Avoids Blue/Yellow confusion. Uses Red/Cyan/Pink.
        # Dark
        self._create_theme_variant(
            "Tritanopia",
            "Dark",
            {
                dpg.mvThemeCol_WindowBg: (30, 20, 20),
                dpg.mvThemeCol_ChildBg: (35, 25, 25),
                dpg.mvThemeCol_PopupBg: (40, 30, 30),
                dpg.mvThemeCol_Border: (120, 100, 100),
                dpg.mvThemeCol_FrameBg: (50, 40, 40),
                dpg.mvThemeCol_TitleBg: (40, 30, 30),
                dpg.mvThemeCol_TitleBgActive: (70, 50, 50),
                dpg.mvThemeCol_MenuBarBg: (40, 30, 30),
                dpg.mvThemeCol_Header: (150, 50, 50),  # Red
                dpg.mvThemeCol_Button: (130, 40, 40),  # Red
                dpg.mvThemeCol_ButtonHovered: (160, 60, 60),
                dpg.mvThemeCol_ButtonActive: (190, 80, 80),
                dpg.mvThemeCol_Text: (230, 230, 230),
            },
        )
        # Light
        self._create_theme_variant(
            "Tritanopia",
            "Light",
            {
                dpg.mvThemeCol_WindowBg: (250, 245, 245),
                dpg.mvThemeCol_ChildBg: (245, 240, 240),
                dpg.mvThemeCol_PopupBg: (255, 255, 255),
                dpg.mvThemeCol_Border: (200, 180, 180),
                dpg.mvThemeCol_FrameBg: (255, 255, 255),
                dpg.mvThemeCol_TitleBg: (240, 230, 230),
                dpg.mvThemeCol_TitleBgActive: (230, 210, 210),
                dpg.mvThemeCol_MenuBarBg: (250, 240, 240),
                dpg.mvThemeCol_Header: (255, 150, 150),  # Light Red
                dpg.mvThemeCol_Button: (255, 220, 220),
                dpg.mvThemeCol_ButtonHovered: (240, 200, 200),
                dpg.mvThemeCol_ButtonActive: (220, 180, 180),
                dpg.mvThemeCol_Text: (30, 10, 10),
            },
        )

    def _create_theme_variant(self, palette, mode, colors):
        tag = f"theme_{palette.lower().replace(' ', '_')}_{mode.lower()}"
        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvAll):
                for col_id, color in colors.items():
                    dpg.add_theme_color(col_id, color, category=dpg.mvThemeCat_Core)

        if palette not in self.themes:
            self.themes[palette] = {}
        self.themes[palette][mode] = tag

    def apply_theme(self, palette=None, mode=None):
        if palette:
            self.current_palette = palette
        if mode:
            self.current_mode = mode

        target_mode = self.current_mode
        if target_mode == "System":
            target_mode = self._get_system_theme()

        # Fallback to Dark if mode not found
        if target_mode not in ["Light", "Dark"]:
            target_mode = "Dark"

        theme_tag = self.themes.get(self.current_palette, {}).get(target_mode)

        # Fallback to Standard Dark if theme not found
        if not theme_tag:
            theme_tag = self.themes["Standard"]["Dark"]

        dpg.bind_theme(theme_tag)

    def _get_system_theme(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "Light" if value == 1 else "Dark"
        except Exception:
            return "Dark"

    def get_profile_status_colors(self):
        # Determine effective mode
        mode = self.current_mode
        if mode == "System":
            mode = self._get_system_theme()

        if mode == "Light":
            return {
                "DEFAULT": (200, 100, 0),  # Darker Orange
                "LOADED": (0, 150, 0),  # Darker Green
            }
        else:
            return {"DEFAULT": (255, 210, 120), "LOADED": (150, 255, 150)}

    def get_log_colors(self):
        # Determine effective mode
        mode = self.current_mode
        if mode == "System":
            mode = self._get_system_theme()

        palette = self.current_palette

        if palette == "Deuteranopia":
            # Blue/Yellow friendly
            return {
                "DEBUG": (150, 150, 150) if mode == "Dark" else (100, 100, 100),
                "INFO": (100, 200, 255) if mode == "Dark" else (0, 100, 200),  # Blue
                "WARNING": (
                    (255, 255, 100) if mode == "Dark" else (200, 180, 0)
                ),  # Yellow
                "ERROR": (
                    (200, 200, 200) if mode == "Dark" else (50, 50, 50)
                ),  # Grey/White (Avoid Red) - Actually user wants distinct.
                # Better Deuteranopia: Error -> Dark Blue/Black vs Warning Yellow?
                # Standard Deuteranopia palettes often use Blue for cool, Yellow for warm.
                # Let's use High Contrast Blue for Error? Or maybe a distinct shape/prefix is better, but we only have color.
                # Let's use a very dark blue or purple for Error.
                "ERROR": (180, 180, 255) if mode == "Dark" else (0, 0, 150),
                "SUCCESS": (
                    (255, 255, 0) if mode == "Dark" else (200, 180, 0)
                ),  # Yellow (Success/Warning might clash? Let's make Success brighter)
            }
        elif palette == "Tritanopia":
            # Red/Cyan friendly
            return {
                "DEBUG": (150, 150, 150) if mode == "Dark" else (100, 100, 100),
                "INFO": (0, 255, 255) if mode == "Dark" else (0, 150, 150),  # Cyan
                "WARNING": (
                    (255, 200, 200) if mode == "Dark" else (200, 100, 100)
                ),  # Light Red
                "ERROR": (255, 0, 0) if mode == "Dark" else (200, 0, 0),  # Red
                "SUCCESS": (0, 200, 200) if mode == "Dark" else (0, 100, 100),  # Teal
            }
        elif palette == "High Contrast":
            return {
                "DEBUG": (200, 200, 200) if mode == "Dark" else (50, 50, 50),
                "INFO": (255, 255, 255) if mode == "Dark" else (0, 0, 0),
                "WARNING": (255, 255, 0) if mode == "Dark" else (150, 150, 0),  # Yellow
                "ERROR": (255, 0, 0) if mode == "Dark" else (200, 0, 0),  # Red
                "SUCCESS": (0, 255, 0) if mode == "Dark" else (0, 150, 0),  # Green
            }
        else:
            # Standard
            if mode == "Light":
                return {
                    "DEBUG": (100, 100, 100),
                    "INFO": (0, 100, 200),
                    "WARNING": (200, 150, 0),
                    "ERROR": (200, 0, 0),
                    "SUCCESS": (0, 150, 0),
                }
            else:
                return {
                    "DEBUG": (170, 170, 170),
                    "INFO": (120, 200, 255),
                    "WARNING": (255, 210, 120),
                    "ERROR": (255, 120, 120),
                    "SUCCESS": (15, 240, 15),
                }


_theme_manager = None


def get_theme_manager():
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
