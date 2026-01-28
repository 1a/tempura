"""Configuration storage and persistence."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .settings import (
    AppSettings,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit,
    get_config_file,
)


class Location(BaseModel):
    """Saved location model."""

    name: str = Field(..., description="Location name (e.g., 'San Francisco, US')")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    country: str = Field(default="", description="Country code")
    is_default: bool = Field(default=False, description="Is this the default location")


class UserPreferences(BaseModel):
    """User preferences model."""

    temperature_unit: TemperatureUnit = TemperatureUnit.FAHRENHEIT
    wind_speed_unit: WindSpeedUnit = WindSpeedUnit.MPH
    time_format: TimeFormat = TimeFormat.TWELVE_HOUR
    auto_refresh_minutes: int = 10
    animations_enabled: bool = True


class ConfigData(BaseModel):
    """Complete configuration data model."""

    api_key: Optional[str] = None
    saved_locations: List[Location] = Field(default_factory=list)
    preferences: UserPreferences = Field(default_factory=UserPreferences)


class ConfigStorage:
    """Manages configuration storage and retrieval."""

    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or get_config_file()
        self._data: Optional[ConfigData] = None

    def load(self) -> ConfigData:
        """Load configuration from file."""
        if self._data is not None:
            return self._data

        if not self.config_file.exists():
            self._data = ConfigData()
            return self._data

        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
            self._data = ConfigData(**data)
        except (json.JSONDecodeError, ValueError) as e:
            self._data = ConfigData()

        return self._data

    def save(self, data: Optional[ConfigData] = None) -> None:
        """Save configuration to file."""
        if data is not None:
            self._data = data

        if self._data is None:
            return

        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        temp_file = self.config_file.with_suffix(".tmp")
        with open(temp_file, "w") as f:
            json.dump(
                self._data.model_dump(mode="json"),
                f,
                indent=2,
                ensure_ascii=False,
            )

        temp_file.replace(self.config_file)

    def get_api_key(self, settings: Optional[AppSettings] = None) -> Optional[str]:
        """Get API key from config or settings."""
        data = self.load()

        if data.api_key:
            return data.api_key

        if settings and settings.openweather_api_key:
            return settings.openweather_api_key

        return None

    def set_api_key(self, api_key: str) -> None:
        """Set API key in configuration."""
        data = self.load()
        data.api_key = api_key
        self.save(data)

    def get_locations(self) -> List[Location]:
        """Get all saved locations."""
        data = self.load()
        return data.saved_locations

    def add_location(self, location: Location) -> None:
        """Add a new location."""
        data = self.load()

        if location.is_default:
            for loc in data.saved_locations:
                loc.is_default = False

        if location not in data.saved_locations:
            data.saved_locations.append(location)

        self.save(data)

    def remove_location(self, location_name: str) -> bool:
        """Remove a location by name."""
        data = self.load()

        original_count = len(data.saved_locations)
        data.saved_locations = [
            loc for loc in data.saved_locations if loc.name != location_name
        ]

        if len(data.saved_locations) < original_count:
            self.save(data)
            return True

        return False

    def set_default_location(self, location_name: str) -> bool:
        """Set a location as default."""
        data = self.load()

        found = False
        for loc in data.saved_locations:
            if loc.name == location_name:
                loc.is_default = True
                found = True
            else:
                loc.is_default = False

        if found:
            self.save(data)

        return found

    def get_default_location(self) -> Optional[Location]:
        """Get the default location."""
        data = self.load()

        for loc in data.saved_locations:
            if loc.is_default:
                return loc

        if data.saved_locations:
            return data.saved_locations[0]

        return None

    def get_preferences(self) -> UserPreferences:
        """Get user preferences."""
        data = self.load()
        return data.preferences

    def update_preferences(self, preferences: UserPreferences) -> None:
        """Update user preferences."""
        data = self.load()
        data.preferences = preferences
        self.save(data)

    def is_first_run(self) -> bool:
        """Check if this is the first run (no config file exists or no API key set)."""
        if not self.config_file.exists():
            return True

        data = self.load()
        return data.api_key is None or not data.saved_locations
