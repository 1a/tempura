"""Reusable weather card widget."""

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Static

from tempura.assets.ascii_art import get_weather_icon, get_weather_color


class WeatherCard(Widget):
    """A card displaying weather information."""

    def __init__(
        self,
        title: str,
        icon_code: str,
        temperature: str,
        description: str,
        details: dict | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        """
        Initialize weather card.

        Args:
            title: Card title (e.g., "Today", "Tomorrow")
            icon_code: Weather icon code
            temperature: Temperature string
            description: Weather description
            details: Optional dict of additional details
            name: Widget name
            id: Widget ID
            classes: Widget classes
        """
        super().__init__(name=name, id=id, classes=classes)
        self.title = title
        self.icon_code = icon_code
        self.temperature = temperature
        self.description = description
        self.details = details or {}

    def update_weather(
        self,
        icon_code: str,
        temperature: str,
        description: str,
        details: dict | None = None,
    ) -> None:
        """Update weather card data."""
        self.icon_code = icon_code
        self.temperature = temperature
        self.description = description
        self.details = details or {}
        self.refresh()

    def render(self) -> RenderableType:
        """Render the weather card."""
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="center")

        icon = get_small_icon(self.icon_code)
        table.add_row(Text(icon, style="bold"))

        table.add_row(Text(self.temperature, style="bold bright_yellow"))

        table.add_row(Text(self.description, style="dim"))

        if self.details:
            table.add_row("")
            for key, value in self.details.items():
                table.add_row(Text(f"{key}: {value}", style="dim"))

        return Panel(
            table,
            title=self.title,
            border_style="blue",
            padding=(1, 2),
        )


class CompactWeatherCard(Widget):
    """A compact weather card for forecast displays."""

    def __init__(
        self,
        day: str,
        date: str,
        icon_code: str,
        temp_high: str,
        temp_low: str,
        description: str = "",
        humidity: str = "",
        wind: str = "",
        precipitation: str = "",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.day = day
        self.date = date
        self.icon_code = icon_code
        self.temp_high = temp_high
        self.temp_low = temp_low
        self.description = description
        self.humidity = humidity
        self.wind = wind
        self.precipitation = precipitation

    def render(self) -> RenderableType:
        """Render compact weather card."""
        icon_lines = get_weather_icon(self.icon_code)
        icon_color = get_weather_color(self.icon_code)

        table = Table.grid(padding=(0, 0))
        table.add_column(justify="center")

        table.add_row(Text(self.day, style="bold white"))
        table.add_row(Text(self.date, style="dim"))
        for line in icon_lines:
            table.add_row(Text(line, style=icon_color))
        table.add_row(Text(f"H: {self.temp_high}", style="bright_red"))
        table.add_row(Text(f"L: {self.temp_low}", style="bright_blue"))
        table.add_row(Text(self.description, style="dim"))
        table.add_row(Text(f"Hum: {self.humidity}", style="cyan"))
        table.add_row(Text(f"Wind: {self.wind}", style="green"))
        table.add_row(Text(f"Rain: {self.precipitation}", style="blue"))

        return table
