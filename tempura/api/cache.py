"""Simple in-memory cache for API responses."""

import time
from typing import Any, Dict, Optional, Tuple


class SimpleCache:
    """Thread-safe in-memory cache with TTL."""

    def __init__(self, default_ttl: int = 600):
        """
        Initialize cache.

        Args:
            default_ttl: Default time-to-live in seconds (default: 10 minutes)
        """
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]

        if time.time() > expiry:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        ttl = ttl if ttl is not None else self._default_ttl
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()

    def remove(self, key: str) -> bool:
        """
        Remove a specific cache entry.

        Args:
            key: Cache key

        Returns:
            True if key was removed, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
