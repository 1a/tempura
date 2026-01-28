"""Current weather display screen."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical, Grid
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, LoadingIndicator
from textual.reactive import reactive

from tempura.api.client import WeatherAPIError
from tempura.widgets.animated_icon import AnimatedWeatherIcon
from tempura.weather.formatter import WeatherFormatter


class CurrentWeatherScreen(Screen):
    """Display current weather conditions."""

    BINDINGS = [
        ("escape", "app.menu", "Menu"),
        ("m", "app.menu", "Menu"),
        ("r", "refresh", "Refresh"),
    ]

    is_loading = reactive(True)
    error_message = reactive("")

    def compose(self) -> ComposeResult:
        """Compose the weather display."""
        yield Header()

        with Center(classes="weather-screen"):
            with Vertical(classes="weather-content"):
                yield Static(id="location-header", classes="weather-header")
                yield AnimatedWeatherIcon(
                    id="weather-icon",
                    classes="weather-icon-large",
                )
                yield Static(id="temperature", classes="temperature-large")
                yield Static(id="description")

                with Grid(id="details-grid", classes="weather-details"):
                    yield Label("Feels Like:", classes="detail-label")
                    yield Static(id="feels-like", classes="detail-value")

                    yield Label("Humidity:", classes="detail-label")
                    yield Static(id="humidity", classes="detail-value")

                    yield Label("Wind:", classes="detail-label")
                    yield Static(id="wind", classes="detail-value")

                    yield Label("Pressure:", classes="detail-label")
                    yield Static(id="pressure", classes="detail-value")

                    yield Label("Sunrise:", classes="detail-label")
                    yield Static(id="sunrise", classes="detail-value")

                    yield Label("Sunset:", classes="detail-label")
                    yield Static(id="sunset", classes="detail-value")

                yield LoadingIndicator(id="loading")
                yield Static(id="error", classes="error-message")

        yield Footer()

    async def on_mount(self) -> None:
        """Load weather data when screen mounts."""
        await self.refresh_data()

        auto_refresh = self.app.storage.get_preferences().auto_refresh_minutes
        if auto_refresh > 0:
            self.set_interval(auto_refresh * 60, self.refresh_data)

    async def refresh_data(self) -> None:
        """Refresh weather data."""
        self.is_loading = True
        self.error_message = ""
        self.query_one("#loading", LoadingIndicator).display = True
        self.query_one("#error", Static).display = False

        try:
            location = self.app.storage.get_default_location()

            if not location:
                self.error_message = "No default location set. Please add a location in settings."
                raise ValueError("No location")

            if not self.app.api_client:
                self.error_message = "No API key configured. Please set your API key in settings."
                raise ValueError("No API key")

            weather = await self.app.api_client.get_current_weather(
                location.lat, location.lon
            )

            preferences = self.app.storage.get_preferences()
            formatter = WeatherFormatter(
                temperature_unit=preferences.temperature_unit,
                wind_speed_unit=preferences.wind_speed_unit,
                time_format=preferences.time_format,
            )

            data = formatter.format_current_weather(weather)

            self.query_one("#location-header", Static).update(
                f"{data['location']}, {data['country']}"
            )

            icon_widget = self.query_one("#weather-icon", AnimatedWeatherIcon)
            icon_widget.set_icon(data['icon_code'])
            icon_widget.enable_animation(preferences.animations_enabled)

            self.query_one("#temperature", Static).update(data['temperature'])
            self.query_one("#description", Static).update(data['description'])
            self.query_one("#feels-like", Static).update(data['feels_like'])
            self.query_one("#humidity", Static).update(data['humidity'])
            self.query_one("#wind", Static).update(data['wind'])
            self.query_one("#pressure", Static).update(data['pressure'])
            self.query_one("#sunrise", Static).update(data['sunrise'])
            self.query_one("#sunset", Static).update(data['sunset'])

            self.is_loading = False

        except WeatherAPIError as e:
            self.error_message = f"Weather API error: {str(e)}"
            self.is_loading = False

        except Exception as e:
            if not self.error_message:
                self.error_message = f"Error loading weather: {str(e)}"
            self.is_loading = False

        finally:
            self.query_one("#loading", LoadingIndicator).display = self.is_loading
            error_widget = self.query_one("#error", Static)
            if self.error_message:
                error_widget.update(self.error_message)
                error_widget.display = True
            else:
                error_widget.display = False

    def action_refresh(self) -> None:
        """Handle refresh action."""
        self.run_worker(self.refresh_data())
