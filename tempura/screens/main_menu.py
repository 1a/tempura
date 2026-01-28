"""Main menu screen."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static
from rich.text import Text

from tempura.assets.ascii_art import LOGO_ASCII


class MainMenuScreen(Screen):
    """Main menu screen with navigation options."""

    BINDINGS = [
        ("escape", "app.quit", "Quit"),
        ("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the main menu."""
        yield Header()

        with Center(classes="menu-container"):
            with Vertical():
                yield Static(self._render_logo(), classes="menu-header")

                menu_items = ListView(
                    ListItem(Label("🌤️  Current Weather"), id="current-weather"),
                    ListItem(Label("📅  5-Day Forecast"), id="forecast"),
                    ListItem(Label("⏰  Hourly Forecast"), id="hourly"),
                    ListItem(Label("📍  Manage Locations"), id="locations"),
                    ListItem(Label("⚙️   Settings"), id="settings"),
                    ListItem(Label("❌  Exit"), id="exit"),
                    classes="menu-list",
                )
                yield menu_items

        yield Footer()

    def _render_logo(self) -> Text:
        """Render the logo ASCII art."""
        text = Text()
        for line in LOGO_ASCII:
            text.append(line + "\n", style="bold cyan")
        return text

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle menu item selection."""
        item_id = event.item.id

        if item_id == "current-weather":
            from tempura.screens.current_weather import CurrentWeatherScreen
            self.app.push_screen(CurrentWeatherScreen())

        elif item_id == "forecast":
            from tempura.screens.forecast import ForecastScreen
            self.app.push_screen(ForecastScreen())

        elif item_id == "hourly":
            from tempura.screens.hourly import HourlyForecastScreen
            self.app.push_screen(HourlyForecastScreen())

        elif item_id == "locations":
            from tempura.screens.locations import LocationsScreen
            self.app.push_screen(LocationsScreen())

        elif item_id == "settings":
            from tempura.screens.settings import SettingsScreen
            self.app.push_screen(SettingsScreen())

        elif item_id == "exit":
            self.app.exit()
