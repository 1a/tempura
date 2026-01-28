"""Animation frames for weather effects."""

from typing import Dict, List

RAIN_ANIMATION_FRAMES: List[List[str]] = [
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
    ],
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "  ‚ʻ‚ʻ‚ʻ‚ʻ   ",
        "  ‚ʻ‚ʻ‚ʻ‚ʻ   ",
    ],
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "   ‚ʻ‚ʻ‚ʻ‚ʻ  ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
    ],
]

SNOW_ANIMATION_FRAMES: List[List[str]] = [
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "   *  *  *   ",
        "  *  *  *    ",
    ],
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "  *  *  *    ",
        "   *  *  *   ",
    ],
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        " *  *  *     ",
        "  *  *  *    ",
    ],
]

THUNDERSTORM_ANIMATION_FRAMES: List[List[str]] = [
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "   ⚡ʻ‚ʻ‚ʻ   ",
        "  ‚ʻ⚡ʻ‚ʻ    ",
    ],
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "  ‚ʻ‚ʻ⚡ʻ    ",
        "   ⚡ʻ‚ʻ‚ʻ   ",
    ],
    [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
    ],
]

CLOUD_ANIMATION_FRAMES: List[List[str]] = [
    [
        "             ",
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__)__) ",
        "             ",
    ],
    [
        "             ",
        "    .--.     ",
        "  -(    ).   ",
        " (___.__)__) ",
        "             ",
    ],
    [
        "             ",
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__)__) ",
        "             ",
    ],
]

MIST_ANIMATION_FRAMES: List[List[str]] = [
    [
        "             ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
    ],
    [
        "             ",
        "  ≡ ≡ ≡ ≡   ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
        " ≡ ≡ ≡ ≡ ≡  ",
    ],
    [
        "             ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
    ],
]

ANIMATION_MAP: Dict[str, List[List[str]]] = {
    "rain": RAIN_ANIMATION_FRAMES,
    "shower_rain": RAIN_ANIMATION_FRAMES,
    "snow": SNOW_ANIMATION_FRAMES,
    "thunderstorm": THUNDERSTORM_ANIMATION_FRAMES,
    "scattered_clouds": CLOUD_ANIMATION_FRAMES,
    "broken_clouds": CLOUD_ANIMATION_FRAMES,
    "mist": MIST_ANIMATION_FRAMES,
    "fog": MIST_ANIMATION_FRAMES,
}


def get_animation_frames(weather_key: str) -> List[List[str]]:
    """
    Get animation frames for a weather condition.

    Args:
        weather_key: Weather condition key (e.g., 'rain', 'snow')

    Returns:
        List of animation frames (each frame is a list of strings)
    """
    return ANIMATION_MAP.get(weather_key, [])


def has_animation(weather_key: str) -> bool:
    """
    Check if a weather condition has animation.

    Args:
        weather_key: Weather condition key

    Returns:
        True if animation exists
    """
    return weather_key in ANIMATION_MAP
