"""Pydantic models for OpenWeatherMap API responses."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Geographic coordinates."""

    lat: float
    lon: float


class WeatherCondition(BaseModel):
    """Weather condition details."""

    id: int
    main: str
    description: str
    icon: str


class CurrentWeatherData(BaseModel):
    """Current weather data."""

    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class Wind(BaseModel):
    """Wind information."""

    speed: float
    deg: int
    gust: Optional[float] = None


class Clouds(BaseModel):
    """Cloud coverage."""

    all: int


class Rain(BaseModel):
    """Rain volume."""

    one_hour: Optional[float] = Field(default=None, alias="1h")
    three_hours: Optional[float] = Field(default=None, alias="3h")


class Snow(BaseModel):
    """Snow volume."""

    one_hour: Optional[float] = Field(default=None, alias="1h")
    three_hours: Optional[float] = Field(default=None, alias="3h")


class Sys(BaseModel):
    """System data."""

    type: Optional[int] = None
    id: Optional[int] = None
    country: Optional[str] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None


class CurrentWeather(BaseModel):
    """Complete current weather response."""

    coord: Coordinates
    weather: List[WeatherCondition]
    base: str
    main: CurrentWeatherData
    visibility: Optional[int] = None
    wind: Wind
    clouds: Clouds
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int

    @property
    def primary_condition(self) -> WeatherCondition:
        """Get the primary weather condition."""
        return self.weather[0] if self.weather else WeatherCondition(
            id=0, main="Unknown", description="Unknown", icon="01d"
        )

    @property
    def temperature(self) -> float:
        """Get temperature in Kelvin."""
        return self.main.temp

    @property
    def feels_like_temp(self) -> float:
        """Get 'feels like' temperature in Kelvin."""
        return self.main.feels_like


class HourlyWeatherData(BaseModel):
    """Hourly forecast data point."""

    dt: int
    main: CurrentWeatherData
    weather: List[WeatherCondition]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    sys: Optional[dict] = None
    dt_txt: str

    @property
    def primary_condition(self) -> WeatherCondition:
        """Get the primary weather condition."""
        return self.weather[0] if self.weather else WeatherCondition(
            id=0, main="Unknown", description="Unknown", icon="01d"
        )

    @property
    def timestamp(self) -> datetime:
        """Get datetime from timestamp."""
        return datetime.fromtimestamp(self.dt)


class HourlyForecast(BaseModel):
    """Hourly forecast response (48 hours via 5-day/3-hour API)."""

    cod: str
    message: int
    cnt: int
    list: List[HourlyWeatherData]
    city: dict


class DailyTemp(BaseModel):
    """Daily temperature data."""

    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


class DailyFeelsLike(BaseModel):
    """Daily 'feels like' temperatures."""

    day: float
    night: float
    eve: float
    morn: float


class DailyWeatherData(BaseModel):
    """Daily forecast data point."""

    dt: int
    sunrise: Optional[int] = None
    sunset: Optional[int] = None
    temp: DailyTemp
    feels_like: DailyFeelsLike
    pressure: int
    humidity: int
    weather: List[WeatherCondition]
    speed: float
    deg: int
    gust: Optional[float] = None
    clouds: int
    pop: float
    rain: Optional[float] = None
    snow: Optional[float] = None

    @property
    def primary_condition(self) -> WeatherCondition:
        """Get the primary weather condition."""
        return self.weather[0] if self.weather else WeatherCondition(
            id=0, main="Unknown", description="Unknown", icon="01d"
        )

    @property
    def date(self) -> datetime:
        """Get date from timestamp."""
        return datetime.fromtimestamp(self.dt)


class DailyForecast(BaseModel):
    """Daily forecast response (7-16 days)."""

    city: dict
    cod: str
    message: float
    cnt: int
    list: List[DailyWeatherData]


class GeocodingResult(BaseModel):
    """Geocoding API result."""

    name: str
    local_names: Optional[dict] = None
    lat: float
    lon: float
    country: str
    state: Optional[str] = None

    @property
    def display_name(self) -> str:
        """Get formatted display name."""
        if self.state:
            return f"{self.name}, {self.state}, {self.country}"
        return f"{self.name}, {self.country}"
