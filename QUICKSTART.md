# Quick Start Guide

## Installation Steps

### 1. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or with pip:

```bash
pip install poetry
```

### 2. Install Dependencies

```bash
cd /Users/vali/code/tempura
poetry install
```

### 3. Get Your API Key

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key (free tier)

### 4. Run Tempura

```bash
poetry run tempura
```

The first time you run it, you'll see a setup wizard that will ask for:
- Your OpenWeatherMap API key
- Your default location (e.g., "San Francisco" or "London, UK")

## Alternative: Without Poetry

If you prefer not to use Poetry:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies manually
pip install textual rich httpx pydantic pydantic-settings python-dotenv typer platformdirs

# Run the app
python -m tempura
```

## Keyboard Shortcuts

### Global
- `q` - Quit
- `m` / `Esc` - Return to main menu
- `r` - Refresh
- `?` - Help

### Navigation
- Arrow keys - Navigate menus/lists
- Enter - Select item
- Tab - Move between widgets

### Location Management
- `a` - Add location
- `d` - Delete location
- `s` - Set as default

## Features to Try

1. **Current Weather** - See real-time weather with animated ASCII art
2. **7-Day Forecast** - Browse daily predictions
3. **Hourly Forecast** - Check hour-by-hour weather
4. **Manage Locations** - Add multiple cities
5. **Settings** - Customize units and preferences

## Troubleshooting

If you encounter issues:

1. **Poetry not found**: Install Poetry first (see step 1)
2. **API key error**: Make sure you completed the setup wizard
3. **Location not found**: Try a different format (e.g., "City, Country")
4. **Import errors**: Run `poetry install` to ensure all dependencies are installed

## Testing

To run the app in development mode:

```bash
poetry run python -m tempura
```

Or use the CLI for quick weather checks:

```bash
# Current weather
poetry run python -m tempura.cli current "San Francisco"

# 7-day forecast
poetry run python -m tempura.cli forecast "London" --days 7
```

Enjoy! ☀️
