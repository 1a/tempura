# Installation Guide

## Quick Install (Recommended)

Run the installation script:

```bash
cd /Users/vali/code/tempura
./install.sh
```

This will install Tempura as a system-wide command you can run from anywhere!

---

## Manual Installation Methods

### Method 1: Using pip (Simple)

```bash
cd /Users/vali/code/tempura
pip3 install -e .
```

✅ After this, you can run:
- `tempura` - Interactive TUI app
- `tempura-cli current "San Francisco"` - Quick weather check

### Method 2: Using Poetry (For development)

```bash
# Install Poetry first
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
cd /Users/vali/code/tempura
poetry install

# Run the app
poetry run tempura
```

### Method 3: Using pipx (Isolated install)

```bash
# Install pipx if you don't have it
pip3 install pipx
pipx ensurepath

# Install Tempura
cd /Users/vali/code/tempura
pipx install -e .
```

---

## Verifying Installation

After installation, test that it works:

```bash
# Check that the command exists
which tempura

# Run the app
tempura
```

You should see the setup wizard!

---

## Commands Available

Once installed, you'll have two commands:

### 1. `tempura` - Interactive TUI App

```bash
tempura
```

Full-featured weather app with:
- Beautiful ASCII art animations
- Current weather, 7-day forecast, hourly forecast
- Location management
- Settings

### 2. `tempura-cli` - Quick CLI Commands

```bash
# Current weather
tempura-cli current "San Francisco"
tempura-cli current "London" --unit celsius

# Forecast
tempura-cli forecast "Tokyo" --days 7
tempura-cli forecast "Paris" --unit celsius --days 5
```

---

## Uninstalling

To remove Tempura:

```bash
pip3 uninstall tempura
```

Or with pipx:

```bash
pipx uninstall tempura
```

---

## Troubleshooting

### "command not found: tempura"

After installing, you may need to:

1. **Restart your terminal**, or
2. **Update your PATH**:
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   export PATH="$HOME/.local/bin:$PATH"

   # Then reload
   source ~/.zshrc  # or source ~/.bashrc
   ```

### "No module named 'tempura'"

Make sure you're in the correct directory:
```bash
cd /Users/vali/code/tempura
pip3 install -e .
```

### Permission errors

If you get permission errors, try:
```bash
pip3 install --user -e .
```

Or use `pipx` for an isolated installation.

---

## Development Setup

For development work:

```bash
cd /Users/vali/code/tempura

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or with Poetry
poetry install
poetry shell
```

Now you can edit the code and changes will be reflected immediately!

---

## Next Steps

1. **Get an API key**: https://openweathermap.org/api (free tier)
2. **Run the app**: `tempura`
3. **Complete setup wizard**: Enter your API key and default location
4. **Enjoy!** ☀️

For more help, see:
- **README.md** - Full documentation
- **TROUBLESHOOTING.md** - Common issues
- **QUICKSTART.md** - Quick start guide
