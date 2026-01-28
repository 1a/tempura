"""7-day forecast screen."""

from textual.app import ComposeResult
from textual.containers import Grid, Center, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, LoadingIndicator

from tempura.api.client import WeatherAPIError
from tempura.widgets.weather_card import CompactWeatherCard
from tempura.weather.formatter import WeatherFormatter


class ForecastScreen(Screen):
    """Display 7-day weather forecast."""

    BINDINGS = [
        ("escape", "app.menu", "Menu"),
        ("m", "app.menu", "Menu"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the forecast display."""
        yield Header()

        with Center(classes="weather-screen"):
            with Vertical(classes="weather-content"):
                yield Static("7-Day Forecast", classes="weather-header")
                with Grid(id="forecast-cards", classes="forecast-grid"):
                    pass
                yield LoadingIndicator(id="loading")
                yield Static(id="error", classes="error-message")

        yield Footer()

    async def on_mount(self) -> None:
        """Load forecast data when screen mounts."""
        await self.refresh_data()

    async def refresh_data(self) -> None:
        """Refresh forecast data."""
        self.query_one("#loading", LoadingIndicator).display = True
        self.query_one("#error", Static).display = False

        try:
            location = self.app.storage.get_default_location()

            if not location:
                raise ValueError("No default location set")

            if not self.app.api_client:
                raise ValueError("No API key configured")

            forecast = await self.app.api_client.get_daily_forecast(
                location.lat, location.lon, days=7
            )

            preferences = self.app.storage.get_preferences()
            formatter = WeatherFormatter(
                temperature_unit=preferences.temperature_unit,
                wind_speed_unit=preferences.wind_speed_unit,
                time_format=preferences.time_format,
            )

            container = self.query_one("#forecast-cards", Grid)
            await container.remove_children()

            num_days = len(forecast.list)
            header = self.query_one(".weather-header", Static)
            header.update(f"{num_days}-Day Forecast")

            container.styles.grid_size_columns = num_days

            for day_data in forecast.list:
                data = formatter.format_daily_weather(day_data)

                card = CompactWeatherCard(
                    day=data['day'],
                    date=data['date'],
                    icon_code=data['icon_code'],
                    temp_high=data['temp_max'],
                    temp_low=data['temp_min'],
                    description=data['description'],
                    humidity=data['humidity'],
                    wind=data['wind'],
                    precipitation=data['precipitation'],
                    classes="forecast-card",
                )

                await container.mount(card)

        except WeatherAPIError as e:
            error_widget = self.query_one("#error", Static)
            error_widget.update(f"Weather API error: {str(e)}")
            error_widget.display = True

        except Exception as e:
            error_widget = self.query_one("#error", Static)
            error_widget.update(f"Error loading forecast: {str(e)}")
            error_widget.display = True

        finally:
            self.query_one("#loading", LoadingIndicator).display = False

    def action_refresh(self) -> None:
        """Handle refresh action."""
        self.run_worker(self.refresh_data())
