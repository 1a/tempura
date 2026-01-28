"""Weather data formatting utilities."""

from datetime import datetime
from typing import Optional

from tempura.api.models import CurrentWeather, DailyWeatherData, HourlyWeatherData
from tempura.config.settings import TemperatureUnit, TimeFormat, WindSpeedUnit
from .units import format_temperature, format_wind_speed, degrees_to_cardinal


class WeatherFormatter:
    """Formats weather data for display."""

    def __init__(
        self,
        temperature_unit: TemperatureUnit = TemperatureUnit.FAHRENHEIT,
        wind_speed_unit: WindSpeedUnit = WindSpeedUnit.MPH,
        time_format: TimeFormat = TimeFormat.TWELVE_HOUR,
    ):
        self.temperature_unit = temperature_unit
        self.wind_speed_unit = wind_speed_unit
        self.time_format = time_format

    def format_temp(self, temp: float) -> str:
        """Format temperature."""
        return format_temperature(temp, self.temperature_unit, from_unit="celsius")

    def format_wind(self, speed: float, degrees: Optional[int] = None) -> str:
        """Format wind speed and direction."""
        wind_str = format_wind_speed(speed, self.wind_speed_unit, from_unit="ms")

        if degrees is not None:
            cardinal = degrees_to_cardinal(degrees)
            return f"{wind_str} {cardinal}"

        return wind_str

    def format_time(self, timestamp: int) -> str:
        """Format timestamp to time string."""
        dt = datetime.fromtimestamp(timestamp)

        if self.time_format == TimeFormat.TWELVE_HOUR:
            return dt.strftime("%I:%M %p")
        else:
            return dt.strftime("%H:%M")

    def format_date(self, timestamp: int, include_day: bool = True) -> str:
        """Format timestamp to date string."""
        dt = datetime.fromtimestamp(timestamp)

        if include_day:
            return dt.strftime("%A, %B %d")
        else:
            return dt.strftime("%B %d")

    def format_day_name(self, timestamp: int) -> str:
        """Get day name from timestamp."""
        dt = datetime.fromtimestamp(timestamp)
        today = datetime.now().date()

        if dt.date() == today:
            return "Today"
        elif (dt.date() - today).days == 1:
            return "Tomorrow"
        else:
            return dt.strftime("%A")

    def format_humidity(self, humidity: int) -> str:
        """Format humidity percentage."""
        return f"{humidity}%"

    def format_pressure(self, pressure: int) -> str:
        """Format pressure in hPa."""
        return f"{pressure} hPa"

    def format_visibility(self, visibility: int) -> str:
        """Format visibility in km or miles."""
        if self.wind_speed_unit == WindSpeedUnit.MPH:
            miles = visibility / 1609.34
            return f"{miles:.1f} mi"
        else:
            km = visibility / 1000
            return f"{km:.1f} km"

    def format_precipitation(self, pop: float) -> str:
        """Format precipitation probability."""
        return f"{int(pop * 100)}%"

    def format_current_weather(self, weather: CurrentWeather) -> dict:
        """
        Format current weather for display.

        Returns:
            Dictionary with formatted values
        """
        condition = weather.primary_condition

        return {
            "location": weather.name,
            "country": weather.sys.country or "",
            "temperature": self.format_temp(weather.main.temp),
            "feels_like": self.format_temp(weather.main.feels_like),
            "temp_min": self.format_temp(weather.main.temp_min),
            "temp_max": self.format_temp(weather.main.temp_max),
            "description": condition.description.title(),
            "icon_code": condition.icon,
            "humidity": self.format_humidity(weather.main.humidity),
            "pressure": self.format_pressure(weather.main.pressure),
            "wind": self.format_wind(weather.wind.speed, weather.wind.deg),
            "visibility": (
                self.format_visibility(weather.visibility)
                if weather.visibility
                else "N/A"
            ),
            "sunrise": self.format_time(weather.sys.sunrise) if weather.sys.sunrise else "N/A",
            "sunset": self.format_time(weather.sys.sunset) if weather.sys.sunset else "N/A",
            "timestamp": self.format_time(weather.dt),
        }

    def format_hourly_weather(self, weather: HourlyWeatherData) -> dict:
        """Format hourly weather data."""
        condition = weather.primary_condition

        return {
            "time": self.format_time(weather.dt),
            "temperature": self.format_temp(weather.main.temp),
            "description": condition.description.title(),
            "icon_code": condition.icon,
            "precipitation": self.format_precipitation(weather.pop),
            "wind": self.format_wind(weather.wind.speed, weather.wind.deg),
            "humidity": self.format_humidity(weather.main.humidity),
        }

    def format_daily_weather(self, weather: DailyWeatherData) -> dict:
        """Format daily weather data."""
        condition = weather.primary_condition

        return {
            "day": self.format_day_name(weather.dt),
            "date": self.format_date(weather.dt, include_day=False),
            "temp_max": self.format_temp(weather.temp.max),
            "temp_min": self.format_temp(weather.temp.min),
            "description": condition.description.title(),
            "icon_code": condition.icon,
            "precipitation": self.format_precipitation(weather.pop),
            "wind": self.format_wind(weather.speed, weather.deg),
            "humidity": self.format_humidity(weather.humidity),
        }
