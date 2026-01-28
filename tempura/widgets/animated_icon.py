"""Animated weather icon widget."""

from typing import List

from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget

from tempura.assets.ascii_art import (
    get_weather_icon,
    get_weather_color,
    OPENWEATHER_ICON_MAP,
)
from tempura.assets.animations import (
    get_animation_frames,
    has_animation,
)


class AnimatedWeatherIcon(Widget):
    """Animated weather icon widget with frame-based animation."""

    def __init__(
        self,
        icon_code: str = "01d",
        animation_enabled: bool = True,
        fps: int = 5,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        """
        Initialize animated weather icon.

        Args:
            icon_code: OpenWeatherMap icon code
            animation_enabled: Whether to enable animation
            fps: Frames per second for animation
            name: Widget name
            id: Widget ID
            classes: Widget classes
        """
        super().__init__(name=name, id=id, classes=classes)
        self.icon_code = icon_code
        self.animation_enabled = animation_enabled
        self.fps = fps
        self._current_frame = 0
        self._animation_frames: List[List[str]] = []
        self._timer = None
        self._update_animation_frames()

    def on_mount(self) -> None:
        """Start animation when widget is mounted."""
        if self.animation_enabled and self._animation_frames:
            self._start_animation()

    def on_unmount(self) -> None:
        """Stop animation when widget is unmounted."""
        self._stop_animation()

    def _update_animation_frames(self) -> None:
        """Update animation frames based on current icon."""
        weather_key = OPENWEATHER_ICON_MAP.get(self.icon_code, "scattered_clouds")

        if has_animation(weather_key):
            self._animation_frames = get_animation_frames(weather_key)
        else:
            self._animation_frames = []

    def _start_animation(self) -> None:
        """Start the animation timer."""
        if not self._animation_frames:
            return

        interval = 1.0 / self.fps
        self._timer = self.set_interval(interval, self._animate)

    def _stop_animation(self) -> None:
        """Stop the animation timer."""
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _animate(self) -> None:
        """Advance to next animation frame."""
        if not self._animation_frames:
            return

        self._current_frame = (self._current_frame + 1) % len(self._animation_frames)
        self.refresh()

    def set_icon(self, icon_code: str) -> None:
        """
        Update the weather icon.

        Args:
            icon_code: OpenWeatherMap icon code
        """
        self.icon_code = icon_code
        self._current_frame = 0
        self._update_animation_frames()

        self._stop_animation()
        if self.animation_enabled and self._animation_frames:
            self._start_animation()

        self.refresh()

    def enable_animation(self, enabled: bool = True) -> None:
        """
        Enable or disable animation.

        Args:
            enabled: Whether to enable animation
        """
        self.animation_enabled = enabled

        if enabled and self._animation_frames:
            self._start_animation()
        else:
            self._stop_animation()

        self.refresh()

    def render(self) -> RenderableType:
        """Render the weather icon with current animation frame."""
        if self._animation_frames and self.animation_enabled:
            lines = self._animation_frames[self._current_frame]
        else:
            lines = get_weather_icon(self.icon_code)

        color = get_weather_color(self.icon_code)

        text = Text()
        for i, line in enumerate(lines):
            if i > 0:
                text.append("\n")
            text.append(line, style=color)

        return text
