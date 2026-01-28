"""Main Textual application."""

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding

from tempura.api.client import WeatherAPIClient
from tempura.config.settings import AppSettings
from tempura.config.storage import ConfigStorage


class TempuraApp(App):
    """The main Tempura weather application."""

    CSS_PATH = Path(__file__).parent / "assets" / "styles.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("m", "menu", "Menu"),
        Binding("r", "refresh", "Refresh"),
        Binding("question_mark", "help", "Help"),
    ]

    def __init__(self, **kwargs):
        """Initialize the application."""
        super().__init__(**kwargs)

        self.settings = AppSettings()
        self.storage = ConfigStorage()

        self._api_client: WeatherAPIClient | None = None
        self._is_first_run = self.storage.is_first_run()

    @property
    def api_client(self) -> WeatherAPIClient | None:
        """Get or create API client."""
        if self._api_client is None:
            api_key = self.storage.get_api_key(self.settings)
            if api_key:
                self._api_client = WeatherAPIClient(api_key)
        return self._api_client

    def on_mount(self) -> None:
        """Handle app mount."""
        self.title = "Tempura Weather"
        self.sub_title = "Your Beautiful CLI Weather App"

        if self._is_first_run:
            from tempura.screens.settings import SetupWizardScreen
            self.push_screen(SetupWizardScreen())
        else:
            from tempura.screens.main_menu import MainMenuScreen
            self.push_screen(MainMenuScreen())

    async def on_unmount(self) -> None:
        """Handle app unmount."""
        if self._api_client:
            await self._api_client.close()

    def action_menu(self) -> None:
        """Navigate to main menu."""
        from tempura.screens.main_menu import MainMenuScreen

        self.pop_screen()
        if not isinstance(self.screen, MainMenuScreen):
            self.push_screen(MainMenuScreen())

    def action_refresh(self) -> None:
        """Refresh current screen."""
        if hasattr(self.screen, "refresh_data"):
            self.screen.refresh_data()
        else:
            self.refresh()

    def action_help(self) -> None:
        """Show help screen."""
        help_text = """
# Tempura Weather Help

## Global Keybindings
- `q` - Quit application
- `m` / `Esc` - Return to main menu
- `r` - Refresh current screen
- `?` - Show this help screen

## Navigation
- Arrow keys - Navigate menus and lists
- Enter - Select item
- Tab - Move between widgets

## Screens
- **Current Weather** - View current weather conditions
- **7-Day Forecast** - View daily forecast
- **Hourly Forecast** - View hourly forecast
- **Manage Locations** - Add/remove favorite locations
- **Settings** - Configure app preferences

## Tips
- Add multiple locations in Location Management
- Change temperature units in Settings
- Animations can be disabled in Settings for better performance
        """
        from textual.screen import ModalScreen
        from textual.widgets import Static, Button
        from textual.containers import Center, Vertical

        class HelpScreen(ModalScreen):
            """Help modal screen."""

            def compose(self) -> ComposeResult:
                with Vertical(classes="wizard-container"):
                    with Vertical(classes="wizard-content"):
                        yield Static(help_text, classes="wizard-text")
                        with Center():
                            yield Button("Close", variant="primary", id="close-help")

            def on_button_pressed(self) -> None:
                self.app.pop_screen()

        self.push_screen(HelpScreen())


def run():
    """Run the Tempura application."""
    app = TempuraApp()
    app.run()


if __name__ == "__main__":
    run()
