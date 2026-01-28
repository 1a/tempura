"""Hourly forecast screen."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, LoadingIndicator, DataTable

from tempura.api.client import WeatherAPIError
from tempura.assets.ascii_art import get_small_icon
from tempura.weather.formatter import WeatherFormatter


class HourlyForecastScreen(Screen):
    """Display hourly weather forecast."""

    BINDINGS = [
        ("escape", "app.menu", "Menu"),
        ("m", "app.menu", "Menu"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the hourly forecast display."""
        yield Header()

        with Center():
            with Vertical():
                yield Static("48-Hour Forecast", classes="weather-header")

                table = DataTable(id="hourly-table")
                table.add_columns("Time", "Weather", "Temp", "Rain %", "Wind", "Humidity")
                yield table

                yield LoadingIndicator(id="loading")
                yield Static(id="error", classes="error-message")

        yield Footer()

    async def on_mount(self) -> None:
        """Load hourly forecast data when screen mounts."""
        await self.refresh_data()

    async def refresh_data(self) -> None:
        """Refresh hourly forecast data."""
        self.query_one("#loading", LoadingIndicator).display = True
        self.query_one("#error", Static).display = False

        try:
            location = self.app.storage.get_default_location()

            if not location:
                raise ValueError("No default location set")

            if not self.app.api_client:
                raise ValueError("No API key configured")

            forecast = await self.app.api_client.get_hourly_forecast(
                location.lat, location.lon
            )

            preferences = self.app.storage.get_preferences()
            formatter = WeatherFormatter(
                temperature_unit=preferences.temperature_unit,
                wind_speed_unit=preferences.wind_speed_unit,
                time_format=preferences.time_format,
            )

            table = self.query_one("#hourly-table", DataTable)
            table.clear()

            for hour_data in forecast.list[:16]:
                data = formatter.format_hourly_weather(hour_data)

                icon = get_small_icon(data['icon_code'])

                table.add_row(
                    data['time'],
                    f"{icon} {data['description']}",
                    data['temperature'],
                    data['precipitation'],
                    data['wind'],
                    data['humidity'],
                )

        except WeatherAPIError as e:
            error_widget = self.query_one("#error", Static)
            error_widget.update(f"Weather API error: {str(e)}")
            error_widget.display = True

        except Exception as e:
            error_widget = self.query_one("#error", Static)
            error_widget.update(f"Error loading hourly forecast: {str(e)}")
            error_widget.display = True

        finally:
            self.query_one("#loading", LoadingIndicator).display = False

    def action_refresh(self) -> None:
        """Handle refresh action."""
        self.run_worker(self.refresh_data())
