"""CLI commands for non-interactive mode."""

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from tempura.api.client import WeatherAPIClient, WeatherAPIError
from tempura.config.settings import AppSettings, TemperatureUnit, WindSpeedUnit
from tempura.config.storage import ConfigStorage
from tempura.weather.formatter import WeatherFormatter

app = typer.Typer(
    name="tempura",
    help="Beautiful CLI weather application",
    add_completion=False,
)

console = Console()


@app.command("current")
def show_current_weather(
    location: str = typer.Argument(help="Location name (e.g., 'San Francisco')"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="OpenWeatherMap API key"),
    unit: str = typer.Option("fahrenheit", "--unit", help="Temperature unit (celsius/fahrenheit)"),
):
    """Show current weather for a location."""
    storage = ConfigStorage()
    settings = AppSettings()

    key = api_key or storage.get_api_key(settings)
    if not key:
        console.print("[red]Error: API key not found. Set OPENWEATHER_API_KEY or use --api-key[/red]")
        raise typer.Exit(1)

    temp_unit = TemperatureUnit.CELSIUS if unit.lower() == "celsius" else TemperatureUnit.FAHRENHEIT

    async def fetch_weather():
        async with WeatherAPIClient(key) as client:
            try:
                weather, _ = await client.get_weather_for_location(location)

                formatter = WeatherFormatter(temperature_unit=temp_unit)
                data = formatter.format_current_weather(weather)

                table = Table(title=f"Current Weather - {data['location']}, {data['country']}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="yellow")

                table.add_row("Temperature", data['temperature'])
                table.add_row("Feels Like", data['feels_like'])
                table.add_row("Description", data['description'])
                table.add_row("Humidity", data['humidity'])
                table.add_row("Wind", data['wind'])
                table.add_row("Pressure", data['pressure'])

                if data['sunrise'] != "N/A":
                    table.add_row("Sunrise", data['sunrise'])
                if data['sunset'] != "N/A":
                    table.add_row("Sunset", data['sunset'])

                console.print(table)

            except WeatherAPIError as e:
                console.print(f"[red]Error: {e}[/red]")
                raise typer.Exit(1)

    asyncio.run(fetch_weather())


@app.command("forecast")
def show_forecast(
    location: str = typer.Argument(help="Location name"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days (1-7)"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="OpenWeatherMap API key"),
    unit: str = typer.Option("fahrenheit", "--unit", help="Temperature unit"),
):
    """Show forecast for a location."""
    storage = ConfigStorage()
    settings = AppSettings()

    key = api_key or storage.get_api_key(settings)
    if not key:
        console.print("[red]Error: API key not found[/red]")
        raise typer.Exit(1)

    temp_unit = TemperatureUnit.CELSIUS if unit.lower() == "celsius" else TemperatureUnit.FAHRENHEIT

    async def fetch_forecast():
        async with WeatherAPIClient(key) as client:
            try:
                results = await client.geocode_location(location)
                if not results:
                    console.print(f"[red]Location not found: {location}[/red]")
                    raise typer.Exit(1)

                loc = results[0]
                forecast = await client.get_daily_forecast(loc.lat, loc.lon, days=days)

                formatter = WeatherFormatter(temperature_unit=temp_unit)

                table = Table(title=f"{days}-Day Forecast - {loc.display_name}")
                table.add_column("Day", style="cyan")
                table.add_column("High", style="red")
                table.add_column("Low", style="blue")
                table.add_column("Description", style="white")

                for day_data in forecast.list:
                    data = formatter.format_daily_weather(day_data)
                    table.add_row(
                        data['day'],
                        data['temp_max'],
                        data['temp_min'],
                        data['description'],
                    )

                console.print(table)

            except WeatherAPIError as e:
                console.print(f"[red]Error: {e}[/red]")
                raise typer.Exit(1)

    asyncio.run(fetch_forecast())


def main():
    """Main entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
