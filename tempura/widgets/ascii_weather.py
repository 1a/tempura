"""Static ASCII weather icon widget."""

from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget

from tempura.assets.ascii_art import (
    get_weather_icon,
    get_weather_color,
    OPENWEATHER_ICON_MAP,
)


class WeatherIcon(Widget):
    """Static weather icon widget displaying ASCII art."""

    def __init__(
        self,
        icon_code: str = "01d",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        """
        Initialize weather icon.

        Args:
            icon_code: OpenWeatherMap icon code (e.g., '01d', '10n')
            name: Widget name
            id: Widget ID
            classes: Widget classes
        """
        super().__init__(name=name, id=id, classes=classes)
        self.icon_code = icon_code

    def set_icon(self, icon_code: str) -> None:
        """
        Update the weather icon.

        Args:
            icon_code: OpenWeatherMap icon code
        """
        self.icon_code = icon_code
        self.refresh()

    def render(self) -> RenderableType:
        """Render the weather icon."""
        lines = get_weather_icon(self.icon_code)
        color = get_weather_color(self.icon_code)

        text = Text()
        for i, line in enumerate(lines):
            if i > 0:
                text.append("\n")
            text.append(line, style=color)

        return text
