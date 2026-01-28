"""ASCII art definitions for weather conditions."""

from typing import Dict, List

WEATHER_ICONS: Dict[str, List[str]] = {
    "clear_day": [
        "    \\   /    ",
        "     .-.     ",
        "  ‒ (   ) ‒  ",
        "     `-'     ",
        "    /   \\    ",
    ],
    "clear_night": [
        "    *        ",
        "      .-.    ",
        "     (   )   ",
        "      `-'    ",
        "  *       *  ",
    ],
    "few_clouds_day": [
        "   \\  /      ",
        " _ /\"\".-.    ",
        "   \\_(   ).  ",
        "   /(___(__)  ",
        "             ",
    ],
    "few_clouds_night": [
        "    *        ",
        " _ .--.      ",
        "   (    ).   ",
        "   (___(__)  ",
        "  *          ",
    ],
    "scattered_clouds": [
        "             ",
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__)__) ",
        "             ",
    ],
    "broken_clouds": [
        "             ",
        "   .--..--.  ",
        " _(    __(   ",
        "(__(__(_(__) ",
        "             ",
    ],
    "shower_rain": [
        " _`/\"\".-.    ",
        "  ,\\_(   ).  ",
        "   /(___(__)  ",
        "    ʻ‚ʻ‚ʻ‚ʻ   ",
        "    ‚ʻ‚ʻ‚ʻ    ",
    ],
    "rain": [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
        " ‚ʻ‚ʻ‚ʻ‚ʻ    ",
    ],
    "thunderstorm": [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "   ⚡ʻ‚ʻ‚ʻ   ",
        "  ‚ʻ⚡ʻ‚ʻ    ",
    ],
    "snow": [
        "     .-.     ",
        "  .-(   ).   ",
        " (___.__)__) ",
        "   *  *  *   ",
        "  *  *  *    ",
    ],
    "mist": [
        "             ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
        " ≡ ≡ ≡ ≡ ≡  ",
        "  ≡ ≡ ≡ ≡   ",
    ],
    "fog": [
        " ─ ─ ─ ─ ─  ",
        "  ─ ─ ─ ─   ",
        " ─ ─ ─ ─ ─  ",
        "  ─ ─ ─ ─   ",
        " ─ ─ ─ ─ ─  ",
    ],
    "tornado": [
        "             ",
        "      /)     ",
        "    (/ )     ",
        "   (/  )     ",
        "  (____      ",
    ],
}

OPENWEATHER_ICON_MAP: Dict[str, str] = {
    "01d": "clear_day",
    "01n": "clear_night",
    "02d": "few_clouds_day",
    "02n": "few_clouds_night",
    "03d": "scattered_clouds",
    "03n": "scattered_clouds",
    "04d": "broken_clouds",
    "04n": "broken_clouds",
    "09d": "shower_rain",
    "09n": "shower_rain",
    "10d": "rain",
    "10n": "rain",
    "11d": "thunderstorm",
    "11n": "thunderstorm",
    "13d": "snow",
    "13n": "snow",
    "50d": "mist",
    "50n": "fog",
}

WEATHER_CONDITION_COLORS: Dict[str, str] = {
    "clear_day": "yellow",
    "clear_night": "bright_blue",
    "few_clouds_day": "yellow",
    "few_clouds_night": "bright_blue",
    "scattered_clouds": "white",
    "broken_clouds": "bright_black",
    "shower_rain": "blue",
    "rain": "bright_blue",
    "thunderstorm": "bright_yellow",
    "snow": "bright_cyan",
    "mist": "bright_black",
    "fog": "bright_black",
    "tornado": "bright_red",
}

LOGO_ASCII = [
    " ████████╗███████╗███╗   ███╗██████╗ ██╗   ██╗██████╗  █████╗ ",
    " ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██║   ██║██╔══██╗██╔══██╗",
    "    ██║   █████╗  ██╔████╔██║██████╔╝██║   ██║██████╔╝███████║",
    "    ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗██╔══██║",
    "    ██║   ███████╗██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║██║  ██║",
    "    ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝",
    "                  Your Beautiful CLI Weather App                ",
]


def get_weather_icon(icon_code: str) -> List[str]:
    """
    Get ASCII art for weather icon code.

    Args:
        icon_code: OpenWeatherMap icon code (e.g., '01d', '10n')

    Returns:
        List of strings representing ASCII art lines
    """
    weather_key = OPENWEATHER_ICON_MAP.get(icon_code, "scattered_clouds")
    return WEATHER_ICONS[weather_key]


def get_weather_color(icon_code: str) -> str:
    """
    Get color for weather icon code.

    Args:
        icon_code: OpenWeatherMap icon code

    Returns:
        Rich color string
    """
    weather_key = OPENWEATHER_ICON_MAP.get(icon_code, "scattered_clouds")
    return WEATHER_CONDITION_COLORS[weather_key]


def get_small_icon(icon_code: str) -> str:
    """
    Get a small (single character/emoji-like) weather icon.

    Args:
        icon_code: OpenWeatherMap icon code

    Returns:
        Small icon string
    """
    small_icons = {
        "01d": "☀️",
        "01n": "🌙",
        "02d": "🌤️",
        "02n": "🌙",
        "03d": "⛅",
        "03n": "☁️",
        "04d": "☁️",
        "04n": "☁️",
        "09d": "🌧️",
        "09n": "🌧️",
        "10d": "🌦️",
        "10n": "🌧️",
        "11d": "⛈️",
        "11n": "⛈️",
        "13d": "❄️",
        "13n": "❄️",
        "50d": "🌫️",
        "50n": "🌫️",
    }
    return small_icons.get(icon_code, "⛅")
