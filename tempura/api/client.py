"""OpenWeatherMap API client."""

import asyncio
from typing import List, Optional, Tuple

import httpx
from httpx import HTTPStatusError, RequestError

from .cache import SimpleCache
from .models import (
    CurrentWeather,
    DailyForecast,
    GeocodingResult,
    HourlyForecast,
)


class WeatherAPIError(Exception):
    """Base exception for weather API errors."""

    pass


class APIKeyError(WeatherAPIError):
    """Invalid or missing API key."""

    pass


class LocationNotFoundError(WeatherAPIError):
    """Location not found."""

    pass


class RateLimitError(WeatherAPIError):
    """API rate limit exceeded."""

    pass


class WeatherAPIClient:
    """Async client for OpenWeatherMap API."""

    BASE_URL = "https://api.openweathermap.org"
    TIMEOUT = 10.0

    def __init__(self, api_key: str, cache_ttl: int = 600):
        """
        Initialize API client.

        Args:
            api_key: OpenWeatherMap API key
            cache_ttl: Cache time-to-live in seconds (default: 10 minutes)
        """
        if not api_key:
            raise APIKeyError("API key is required")

        self.api_key = api_key
        self._cache = SimpleCache(default_ttl=cache_ttl)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.TIMEOUT)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.TIMEOUT)
        return self._client

    async def _request(self, endpoint: str, params: dict) -> dict:
        """
        Make API request.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            JSON response data

        Raises:
            APIKeyError: Invalid API key
            RateLimitError: Rate limit exceeded
            WeatherAPIError: Other API errors
        """
        params["appid"] = self.api_key
        url = f"{self.BASE_URL}{endpoint}"

        try:
            client = await self._get_client()
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            if e.response.status_code == 401:
                raise APIKeyError("Invalid API key")
            elif e.response.status_code == 404:
                raise LocationNotFoundError("Location not found")
            elif e.response.status_code == 429:
                raise RateLimitError("API rate limit exceeded")
            else:
                raise WeatherAPIError(f"API error: {e.response.status_code}")

        except RequestError as e:
            raise WeatherAPIError(f"Network error: {str(e)}")

    async def get_current_weather(
        self, lat: float, lon: float, use_cache: bool = True
    ) -> CurrentWeather:
        """
        Get current weather data.

        Args:
            lat: Latitude
            lon: Longitude
            use_cache: Whether to use cached data

        Returns:
            Current weather data
        """
        cache_key = f"current:{lat},{lon}"

        if use_cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached

        params = {"lat": lat, "lon": lon, "units": "metric"}
        data = await self._request("/data/2.5/weather", params)
        weather = CurrentWeather(**data)

        self._cache.set(cache_key, weather)
        return weather

    async def get_hourly_forecast(
        self, lat: float, lon: float, use_cache: bool = True
    ) -> HourlyForecast:
        """
        Get hourly forecast (next 48 hours via 5-day/3-hour forecast).

        Args:
            lat: Latitude
            lon: Longitude
            use_cache: Whether to use cached data

        Returns:
            Hourly forecast data
        """
        cache_key = f"hourly:{lat},{lon}"

        if use_cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached

        params = {"lat": lat, "lon": lon, "units": "metric"}
        data = await self._request("/data/2.5/forecast", params)
        forecast = HourlyForecast(**data)

        self._cache.set(cache_key, forecast)
        return forecast

    async def get_daily_forecast(
        self, lat: float, lon: float, days: int = 7, use_cache: bool = True
    ) -> DailyForecast:
        """
        Get daily forecast.

        Note: The free tier API uses the 5-day/3-hour forecast.
        For true daily forecast, a paid subscription is required.
        This method aggregates the 3-hour data into daily summaries.

        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days (max 16 with paid subscription)
            use_cache: Whether to use cached data

        Returns:
            Daily forecast data
        """
        cache_key = f"daily:{lat},{lon}:{days}"

        if use_cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached

        params = {"lat": lat, "lon": lon, "cnt": days, "units": "metric"}

        try:
            data = await self._request("/data/2.5/forecast/daily", params)
            forecast = DailyForecast(**data)
            self._cache.set(cache_key, forecast)
            return forecast
        except (APIKeyError, WeatherAPIError):
            hourly = await self.get_hourly_forecast(lat, lon, use_cache)
            daily_data = self._aggregate_hourly_to_daily(hourly, days)
            self._cache.set(cache_key, daily_data)
            return daily_data

    def _aggregate_hourly_to_daily(
        self, hourly: HourlyForecast, days: int
    ) -> DailyForecast:
        """
        Aggregate hourly forecast into daily forecast.

        This is a fallback for free tier users.
        """
        from collections import defaultdict
        from datetime import datetime

        daily_groups = defaultdict(list)

        for item in hourly.list[:days * 8]:
            date = datetime.fromtimestamp(item.dt).date()
            daily_groups[date].append(item)

        from .models import (
            DailyWeatherData,
            DailyTemp,
            DailyFeelsLike,
        )

        daily_list = []
        for date, items in sorted(daily_groups.items())[:days]:
            temps = [item.main.temp for item in items]
            feels_like = [item.main.feels_like for item in items]

            daily_list.append(
                DailyWeatherData(
                    dt=int(datetime.combine(date, datetime.min.time()).timestamp()),
                    temp=DailyTemp(
                        day=sum(temps) / len(temps),
                        min=min(temps),
                        max=max(temps),
                        night=temps[-1] if temps else 0,
                        eve=temps[-2] if len(temps) > 1 else 0,
                        morn=temps[0] if temps else 0,
                    ),
                    feels_like=DailyFeelsLike(
                        day=sum(feels_like) / len(feels_like),
                        night=feels_like[-1] if feels_like else 0,
                        eve=feels_like[-2] if len(feels_like) > 1 else 0,
                        morn=feels_like[0] if feels_like else 0,
                    ),
                    pressure=items[0].main.pressure,
                    humidity=items[0].main.humidity,
                    weather=items[0].weather,
                    speed=items[0].wind.speed,
                    deg=items[0].wind.deg,
                    clouds=items[0].clouds.all,
                    pop=max(item.pop for item in items),
                )
            )

        return DailyForecast(
            city=hourly.city, cod="200", message=0.0, cnt=len(daily_list), list=daily_list
        )

    async def geocode_location(self, location_name: str) -> List[GeocodingResult]:
        """
        Geocode a location name to coordinates.

        Args:
            location_name: City name or "city,country" or "city,state,country"

        Returns:
            List of geocoding results (may be multiple matches)

        Raises:
            LocationNotFoundError: No results found
        """
        # Normalize common country code variations
        country_code_map = {
            "UK": "GB",
            "USA": "US",
            "United States": "US",
            "United Kingdom": "GB",
        }

        search_query = location_name
        for old_code, new_code in country_code_map.items():
            search_query = search_query.replace(f", {old_code}", f", {new_code}")
            search_query = search_query.replace(f",{old_code}", f",{new_code}")

        cache_key = f"geocode:{location_name.lower()}"

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        params = {"q": search_query, "limit": 5}
        data = await self._request("/geo/1.0/direct", params)

        if not data:
            # Try without country code if original search failed
            if "," in location_name:
                city_only = location_name.split(",")[0].strip()
                params = {"q": city_only, "limit": 5}
                data = await self._request("/geo/1.0/direct", params)

        if not data:
            raise LocationNotFoundError(f"Location not found: {location_name}")

        results = [GeocodingResult(**item) for item in data]
        self._cache.set(cache_key, results, ttl=86400)
        return results

    async def get_weather_for_location(
        self, location_name: str
    ) -> Tuple[CurrentWeather, List[GeocodingResult]]:
        """
        Get weather for a location by name.

        Args:
            location_name: Location to search for

        Returns:
            Tuple of (current weather, geocoding results)
        """
        results = await self.geocode_location(location_name)
        if not results:
            raise LocationNotFoundError(f"Location not found: {location_name}")

        weather = await self.get_current_weather(results[0].lat, results[0].lon)
        return weather, results

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
