"""Unit conversion utilities."""

from tempura.config.settings import TemperatureUnit, WindSpeedUnit


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return (kelvin - 273.15) * 9 / 5 + 32


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def format_temperature(
    temp: float, unit: TemperatureUnit, from_unit: str = "celsius"
) -> str:
    """
    Format temperature with appropriate unit.

    Args:
        temp: Temperature value
        unit: Target unit
        from_unit: Source unit (default: celsius, since API returns celsius)

    Returns:
        Formatted temperature string
    """
    if from_unit == "kelvin":
        if unit == TemperatureUnit.CELSIUS:
            temp = kelvin_to_celsius(temp)
        else:
            temp = kelvin_to_fahrenheit(temp)
    elif from_unit == "celsius" and unit == TemperatureUnit.FAHRENHEIT:
        temp = celsius_to_fahrenheit(temp)
    elif from_unit == "fahrenheit" and unit == TemperatureUnit.CELSIUS:
        temp = fahrenheit_to_celsius(temp)

    symbol = "°F" if unit == TemperatureUnit.FAHRENHEIT else "°C"
    return f"{temp:.0f}{symbol}"


def ms_to_mph(ms: float) -> float:
    """Convert meters per second to miles per hour."""
    return ms * 2.23694


def ms_to_kmh(ms: float) -> float:
    """Convert meters per second to kilometers per hour."""
    return ms * 3.6


def format_wind_speed(speed: float, unit: WindSpeedUnit, from_unit: str = "ms") -> str:
    """
    Format wind speed with appropriate unit.

    Args:
        speed: Wind speed value
        unit: Target unit
        from_unit: Source unit (default: ms for meters/second from API)

    Returns:
        Formatted wind speed string
    """
    if from_unit == "ms":
        if unit == WindSpeedUnit.MPH:
            speed = ms_to_mph(speed)
            return f"{speed:.1f} mph"
        elif unit == WindSpeedUnit.KMH:
            speed = ms_to_kmh(speed)
            return f"{speed:.1f} km/h"
        else:
            return f"{speed:.1f} m/s"

    return f"{speed:.1f}"


def degrees_to_cardinal(degrees: int) -> str:
    """
    Convert wind direction degrees to cardinal direction.

    Args:
        degrees: Wind direction in degrees (0-360)

    Returns:
        Cardinal direction (N, NE, E, SE, S, SW, W, NW)
    """
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return directions[index]
