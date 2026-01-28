# Troubleshooting Guide

## "Invalid API Key" Error

If you're getting an "Invalid API key" error even though you copied it correctly, here are the common causes:

### 1. **New API Key Activation Time** (Most Common!)

**OpenWeatherMap API keys take 10-15 minutes to activate after creation.**

**Solution:**
- Wait 15 minutes after creating your API key
- Have a coffee ☕
- Try again

You can verify your key is ready by checking: https://home.openweathermap.org/api_keys

### 2. **Wrong API Key Type**

Make sure you're using the correct API key:
- ✅ Use the key from "Current Weather Data" API
- ❌ Don't use keys from other OpenWeatherMap products

**Solution:**
- Go to https://home.openweathermap.org/api_keys
- Look for the "Default" or "API key" column
- Copy the entire key (usually 32 characters)

### 3. **Copy-Paste Issues**

Common problems:
- Extra spaces at the beginning or end
- Missing characters
- Line breaks in the middle

**Solution:**
- Copy the key again carefully
- Paste it into a text editor first to check
- Make sure there are no spaces or line breaks
- The key should be one continuous string

### 4. **Free Tier Limitations**

The free tier has limits:
- 60 calls per minute
- 1,000,000 calls per month

**Solution:**
- If you hit the rate limit, wait a minute
- Check your usage at: https://home.openweathermap.org/statistics

### 5. **Account Issues**

Your account must be active and verified.

**Solution:**
- Check your email for verification link
- Make sure your account is active
- Log in to https://home.openweathermap.org/ to verify

## Testing Your API Key

You can test your API key manually before entering it into Tempura:

### Using curl:

```bash
# Replace YOUR_API_KEY with your actual key
curl "https://api.openweathermap.org/data/2.5/weather?lat=37.7749&lon=-122.4194&appid=YOUR_API_KEY"
```

**Expected Result:**
- If your key works, you'll get JSON weather data
- If it's invalid, you'll get: `{"cod":401,"message":"Invalid API key..."}`

### Using the CLI:

Once you get past the setup, you can test with:

```bash
export OPENWEATHER_API_KEY="your_key_here"
poetry run python -m tempura.cli current "San Francisco"
```

## Other Common Issues

### "Location not found" Error

**Solutions:**
- Try just the city name: `"Tokyo"`
- Add the country: `"London, UK"`
- Be more specific: `"Portland, Oregon, US"`
- Use different spellings if applicable

### "No default location set" Error

**Solution:**
- Go to "Manage Locations" from the main menu
- Press `A` to add a location
- Make sure at least one location is saved

### Dependencies Not Installing

**Solution:**
```bash
# Try updating pip first
pip install --upgrade pip

# Then install poetry
pip install poetry

# Then install dependencies
poetry install
```

### App Crashes on Startup

**Solution:**
```bash
# Clear config and start fresh
rm -rf ~/.config/tempura/
rm -rf ~/Library/Application\ Support/tempura/  # macOS
rm -rf %APPDATA%/tempura/  # Windows

# Run setup again
poetry run tempura
```

## Getting More Help

### Check API Status

OpenWeatherMap status page: https://status.openweathermap.org/

### Verify Your Account

1. Log in to: https://home.openweathermap.org/
2. Check "API keys" tab
3. Verify your subscription shows "Free" and is active

### Still Having Issues?

The app now provides detailed error messages. Look for:
- Specific error codes (401 = invalid key, 404 = not found, 429 = rate limit)
- Helpful suggestions in the error message
- Network connectivity issues

### Debug Mode

Run with Python directly to see detailed errors:

```bash
poetry run python -m tempura
```

Any Python errors will be displayed in the terminal.

## Manual Configuration

If the setup wizard keeps failing, you can configure manually:

1. **Create config file**:

   macOS/Linux:
   ```bash
   mkdir -p ~/.config/tempura
   ```

   Windows:
   ```bash
   mkdir %APPDATA%\tempura
   ```

2. **Edit config.json**:

   macOS/Linux: `~/.config/tempura/config.json`

   Windows: `%APPDATA%\tempura\config.json`

   ```json
   {
     "api_key": "your_api_key_here",
     "saved_locations": [
       {
         "name": "San Francisco, US",
         "lat": 37.7749,
         "lon": -122.4194,
         "country": "US",
         "is_default": true
       }
     ],
     "preferences": {
       "temperature_unit": "fahrenheit",
       "wind_speed_unit": "mph",
       "time_format": "12h",
       "auto_refresh_minutes": 10,
       "animations_enabled": true
     }
   }
   ```

3. **Run the app**:
   ```bash
   poetry run tempura
   ```

## Need More Help?

The improved error messages in the app should now give you specific guidance. When you see an error:

1. Read the full error message
2. Follow the numbered suggestions
3. Wait if it mentions activation time
4. Try the suggested alternative formats

If you're still stuck, check that:
- ✅ Python 3.10+ is installed
- ✅ All dependencies are installed (`poetry install`)
- ✅ Your API key is at least 15 minutes old
- ✅ You have internet connectivity
- ✅ You're using the correct API key from OpenWeatherMap

Happy weather checking! ☀️🌧️❄️
