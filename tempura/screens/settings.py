"""Settings and setup wizard screens."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Input, Button, Select, Switch, Label
from textual.validation import Function

from tempura.api.client import WeatherAPIClient, APIKeyError
from tempura.config.settings import TemperatureUnit, WindSpeedUnit, TimeFormat
from tempura.config.storage import UserPreferences, Location


class SetupWizardScreen(Screen):
    """First-run setup wizard."""

    def compose(self) -> ComposeResult:
        """Compose the setup wizard."""
        with Center(classes="wizard-container"):
            with Vertical(classes="wizard-content"):
                yield Static("Welcome to Tempura! ☀️", classes="wizard-title")
                yield Static(
                    "Let's get you set up with your OpenWeatherMap API key.",
                    classes="wizard-text"
                )
                yield Static(
                    "Get a free API key at: https://openweathermap.org/api",
                    classes="wizard-text"
                )

                yield Label("API Key:")
                yield Input(
                    placeholder="Enter your API key...",
                    id="api-key-input",
                    password=True,
                )

                yield Label("Default Location:")
                yield Input(
                    placeholder="e.g., San Francisco or London, UK",
                    id="location-input",
                )

                yield Static(id="error-message", classes="error-message")

                with Center():
                    yield Button("Complete Setup", variant="primary", id="setup-button")
                    yield Button("Exit", variant="default", id="exit-button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "exit-button":
            self.app.exit()

        elif event.button.id == "setup-button":
            api_key = self.query_one("#api-key-input", Input).value.strip()
            location_name = self.query_one("#location-input", Input).value.strip()

            error_widget = self.query_one("#error-message", Static)

            if not api_key:
                error_widget.update("Please enter an API key")
                error_widget.display = True
                return

            if not location_name:
                error_widget.update("Please enter a location")
                error_widget.display = True
                return

            try:
                # Show key info for debugging
                key_preview = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"

                async with WeatherAPIClient(api_key) as client:
                    # First, test the API key with a simple weather call
                    try:
                        await client.get_current_weather(37.7749, -122.4194, use_cache=False)
                    except APIKeyError as e:
                        error_widget.update(
                            f"Invalid API key ({key_preview}, {len(api_key)} chars)\n\n"
                            "Common issues:\n"
                            "1. New keys take 10-15 minutes to activate ⏱️\n"
                            "2. Check for spaces at start/end of key\n"
                            "3. Make sure you copied the entire key\n"
                            "4. Verify at: home.openweathermap.org/api_keys\n\n"
                            f"Error: {str(e)}"
                        )
                        error_widget.display = True
                        return
                    except Exception as e:
                        error_widget.update(
                            f"Network or API error:\n{str(e)}\n\n"
                            "Check your internet connection"
                        )
                        error_widget.display = True
                        return

                    # Now geocode the location
                    try:
                        results = await client.geocode_location(location_name)
                    except Exception as e:
                        error_widget.update(
                            f"Location search failed: {str(e)}\n"
                            "Try a different format (e.g., 'London, UK')"
                        )
                        error_widget.display = True
                        return

                    if not results:
                        error_widget.update(
                            f"Location not found: {location_name}\n"
                            "Try: 'San Francisco' or 'London, UK'"
                        )
                        error_widget.display = True
                        return

                    result = results[0]

                self.app.storage.set_api_key(api_key)

                location = Location(
                    name=result.display_name,
                    lat=result.lat,
                    lon=result.lon,
                    country=result.country,
                    is_default=True,
                )

                self.app.storage.add_location(location)

                from tempura.screens.main_menu import MainMenuScreen
                self.app.switch_screen(MainMenuScreen())

            except APIKeyError as e:
                error_widget.update(
                    f"API Key Error: {str(e)}\n"
                    "Note: New keys take 10-15 minutes to activate!"
                )
                error_widget.display = True

            except Exception as e:
                error_widget.update(f"Unexpected error: {str(e)}")
                error_widget.display = True


class SettingsScreen(Screen):
    """Application settings screen."""

    BINDINGS = [
        ("escape", "app.menu", "Menu"),
        ("m", "app.menu", "Menu"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the settings screen."""
        yield Header()

        with Center(classes="settings-container"):
            with Vertical(classes="settings-form"):
                yield Static("Settings", classes="wizard-title")

                yield Label("API Key:", classes="settings-label")
                yield Input(
                    placeholder="OpenWeatherMap API Key",
                    id="api-key-input",
                    password=True,
                )

                yield Label("Temperature Unit:", classes="settings-label")
                yield Select(
                    options=[
                        ("Fahrenheit", "fahrenheit"),
                        ("Celsius", "celsius"),
                    ],
                    id="temp-unit-select",
                )

                yield Label("Wind Speed Unit:", classes="settings-label")
                yield Select(
                    options=[
                        ("Miles per hour (mph)", "mph"),
                        ("Kilometers per hour (km/h)", "kmh"),
                        ("Meters per second (m/s)", "ms"),
                    ],
                    id="wind-unit-select",
                )

                yield Label("Time Format:", classes="settings-label")
                yield Select(
                    options=[
                        ("12-hour", "12h"),
                        ("24-hour", "24h"),
                    ],
                    id="time-format-select",
                )

                yield Label("Auto-refresh (minutes):", classes="settings-label")
                yield Input(
                    placeholder="10",
                    id="refresh-input",
                    type="integer",
                )

                yield Static("")

                with Horizontal():
                    yield Label("Enable Animations:")
                    yield Switch(id="animations-switch", value=True)

                yield Static("")

                yield Static(id="error-message", classes="error-message")

                with Center():
                    yield Button("Save", variant="primary", id="save-button")
                    yield Button("Cancel", variant="default", id="cancel-button")

        yield Footer()

    def on_mount(self) -> None:
        """Load current settings."""
        current_api_key = self.app.storage.get_api_key(self.app.settings)
        if current_api_key:
            self.query_one("#api-key-input", Input).value = current_api_key

        preferences = self.app.storage.get_preferences()

        self.query_one("#temp-unit-select", Select).value = preferences.temperature_unit.value
        self.query_one("#wind-unit-select", Select).value = preferences.wind_speed_unit.value
        self.query_one("#time-format-select", Select).value = preferences.time_format.value
        self.query_one("#refresh-input", Input).value = str(preferences.auto_refresh_minutes)
        self.query_one("#animations-switch", Switch).value = preferences.animations_enabled

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "cancel-button":
            self.app.action_menu()

        elif event.button.id == "save-button":
            api_key = self.query_one("#api-key-input", Input).value.strip()
            error_widget = self.query_one("#error-message", Static)

            if api_key:
                try:
                    async with WeatherAPIClient(api_key) as client:
                        # Test the API key with a simple call
                        await client.get_current_weather(37.7749, -122.4194, use_cache=False)

                    self.app.storage.set_api_key(api_key)
                    self.app._api_client = None

                except APIKeyError:
                    error_widget.update(
                        "Invalid API key. Please check:\n"
                        "1. Copy the key correctly\n"
                        "2. New keys take 10-15 minutes to activate"
                    )
                    error_widget.display = True
                    return
                except Exception as e:
                    error_widget.update(f"Error testing API key: {str(e)}")
                    error_widget.display = True
                    return

            try:
                refresh_minutes = int(self.query_one("#refresh-input", Input).value or "10")
                if refresh_minutes < 1 or refresh_minutes > 60:
                    error_widget.update("Auto-refresh must be between 1 and 60 minutes")
                    error_widget.display = True
                    return
            except ValueError:
                error_widget.update("Invalid auto-refresh value")
                error_widget.display = True
                return

            preferences = UserPreferences(
                temperature_unit=TemperatureUnit(
                    self.query_one("#temp-unit-select", Select).value
                ),
                wind_speed_unit=WindSpeedUnit(
                    self.query_one("#wind-unit-select", Select).value
                ),
                time_format=TimeFormat(
                    self.query_one("#time-format-select", Select).value
                ),
                auto_refresh_minutes=refresh_minutes,
                animations_enabled=self.query_one("#animations-switch", Switch).value,
            )

            self.app.storage.update_preferences(preferences)

            self.notify("Settings saved successfully")
            self.app.action_menu()
