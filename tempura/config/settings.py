"""Application settings and configuration management."""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from platformdirs import user_config_dir


class TemperatureUnit(str, Enum):
    FAHRENHEIT = "fahrenheit"
    CELSIUS = "celsius"


class WindSpeedUnit(str, Enum):
    MPH = "mph"
    KMH = "kmh"
    MS = "ms"


class TimeFormat(str, Enum):
    TWELVE_HOUR = "12h"
    TWENTY_FOUR_HOUR = "24h"


class AppSettings(BaseSettings):
    """Application settings loaded from environment and config file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        case_sensitive=False,
    )

    openweather_api_key: Optional[str] = Field(
        default=None,
        description="OpenWeatherMap API key"
    )

    default_location: Optional[str] = Field(
        default=None,
        description="Default location name"
    )

    temperature_unit: TemperatureUnit = Field(
        default=TemperatureUnit.FAHRENHEIT,
        description="Temperature unit preference"
    )

    wind_speed_unit: WindSpeedUnit = Field(
        default=WindSpeedUnit.MPH,
        description="Wind speed unit preference"
    )

    time_format: TimeFormat = Field(
        default=TimeFormat.TWELVE_HOUR,
        description="Time format preference"
    )

    auto_refresh_minutes: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Auto-refresh interval in minutes"
    )

    animations_enabled: bool = Field(
        default=True,
        description="Enable weather animations"
    )


def get_config_dir() -> Path:
    """Get the configuration directory for the application."""
    config_dir = Path(user_config_dir("tempura", ensure_exists=True))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"
