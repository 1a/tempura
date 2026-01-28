"""Location management screen."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label, Button, Input

from tempura.api.client import WeatherAPIError, LocationNotFoundError
from tempura.config.storage import Location


class AddLocationModal(ModalScreen):
    """Modal for adding a new location."""

    def compose(self) -> ComposeResult:
        """Compose the add location modal."""
        with Center(classes="wizard-container"):
            with Vertical(classes="wizard-content"):
                yield Static("Add New Location", classes="wizard-title")
                yield Static(
                    "Enter city name (e.g., 'San Francisco' or 'London, UK')",
                    classes="wizard-text"
                )
                yield Input(placeholder="City name...", id="location-input")
                yield Static(id="error-message", classes="error-message")

                with Center():
                    yield Button("Add", variant="primary", id="add-button")
                    yield Button("Cancel", variant="default", id="cancel-button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "cancel-button":
            self.dismiss(None)

        elif event.button.id == "add-button":
            location_input = self.query_one("#location-input", Input)
            location_name = location_input.value.strip()

            if not location_name:
                error_widget = self.query_one("#error-message", Static)
                error_widget.update("Please enter a location name")
                error_widget.display = True
                return

            if not self.app.api_client:
                error_widget = self.query_one("#error-message", Static)
                error_widget.update("No API key configured")
                error_widget.display = True
                return

            error_widget = self.query_one("#error-message", Static)

            try:
                results = await self.app.api_client.geocode_location(location_name)

                if not results:
                    error_widget.update(
                        f"Location not found: {location_name}\n\n"
                        "Try:\n"
                        "• Just city name: 'London'\n"
                        "• With country: 'London, UK'\n"
                        "• More specific: 'Portland, Oregon, US'"
                    )
                    error_widget.display = True
                    return

                result = results[0]

                location = Location(
                    name=result.display_name,
                    lat=result.lat,
                    lon=result.lon,
                    country=result.country,
                    is_default=False,
                )

                self.dismiss(location)

            except LocationNotFoundError as e:
                error_widget.update(
                    f"{str(e)}\n\n"
                    "Tips:\n"
                    "• Check spelling\n"
                    "• Try different format\n"
                    "• Use English names"
                )
                error_widget.display = True

            except WeatherAPIError as e:
                error_widget.update(
                    f"API Error: {str(e)}\n\n"
                    "This might be an API key issue.\n"
                    "Check Settings to verify your API key."
                )
                error_widget.display = True

            except Exception as e:
                error_widget.update(
                    f"Unexpected error: {str(e)}\n\n"
                    "Please check your internet connection\n"
                    "and API key in Settings."
                )
                error_widget.display = True


class LocationsScreen(Screen):
    """Manage saved locations."""

    BINDINGS = [
        ("escape", "app.menu", "Menu"),
        ("m", "app.menu", "Menu"),
        ("a", "add_location", "Add"),
        ("d", "delete_location", "Delete"),
        ("s", "set_default", "Set Default"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the locations screen."""
        yield Header()

        with Center():
            with Vertical():
                yield Static("Manage Locations", classes="weather-header")

                yield ListView(id="locations-list", classes="location-list")

                yield Static(
                    "A: Add | D: Delete | S: Set Default | Enter: Select",
                    classes="info-message"
                )

        yield Footer()

    def on_mount(self) -> None:
        """Load locations when screen mounts."""
        self.refresh_list()

    def refresh_list(self) -> None:
        """Refresh the locations list."""
        locations = self.app.storage.get_locations()
        locations_list = self.query_one("#locations-list", ListView)

        # Remove all children manually to avoid ID conflicts
        locations_list.clear()

        # Give it a moment to clear
        if not locations:
            locations_list.append(
                ListItem(Label("No locations saved. Press 'A' to add one."))
            )
            return

        for location in locations:
            prefix = "⭐ " if location.is_default else "   "
            label_text = f"{prefix}{location.name}"

            # Don't use IDs for list items - we'll use index-based lookup
            locations_list.append(
                ListItem(Label(label_text))
            )

    def action_add_location(self) -> None:
        """Add a new location."""
        def handle_result(location: Location | None) -> None:
            if location:
                self.app.storage.add_location(location)
                self.refresh_list()
                self.notify(f"Added {location.name}")

        self.app.push_screen(AddLocationModal(), handle_result)

    def action_delete_location(self) -> None:
        """Delete the selected location."""
        locations_list = self.query_one("#locations-list", ListView)

        if locations_list.index is None:
            self.notify("No location selected", severity="warning")
            return

        locations = self.app.storage.get_locations()

        if not locations or locations_list.index >= len(locations):
            return

        location = locations[locations_list.index]

        if self.app.storage.remove_location(location.name):
            self.refresh_list()
            self.notify(f"Removed {location.name}")

    def action_set_default(self) -> None:
        """Set the selected location as default."""
        locations_list = self.query_one("#locations-list", ListView)

        if locations_list.index is None:
            self.notify("No location selected", severity="warning")
            return

        locations = self.app.storage.get_locations()

        if not locations or locations_list.index >= len(locations):
            return

        location = locations[locations_list.index]

        if self.app.storage.set_default_location(location.name):
            self.refresh_list()
            self.notify(f"Set {location.name} as default")

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle location selection."""
        locations = self.app.storage.get_locations()

        if not locations:
            return

        locations_list = self.query_one("#locations-list", ListView)

        if locations_list.index is not None and locations_list.index < len(locations):
            location = locations[locations_list.index]

            if self.app.storage.set_default_location(location.name):
                self.refresh_list()
                self.notify(f"Selected {location.name}")
