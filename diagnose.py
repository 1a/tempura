#!/usr/bin/env python3
"""Diagnostic tool for Tempura - tests API key and endpoints."""

import asyncio
import sys
import httpx


async def test_weather_api(api_key: str):
    """Test weather API endpoint."""
    print("\n🌤️  Testing Weather API...")
    print("-" * 60)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": 37.7749, "lon": -122.4194, "appid": api_key, "units": "metric"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Weather API works!")
                print(f"   Location: {data['name']}")
                print(f"   Temperature: {data['main']['temp']}°C")
                return True
            else:
                print(f"❌ Weather API failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Weather API error: {e}")
        return False


async def test_geocoding_api(api_key: str):
    """Test geocoding API endpoint."""
    print("\n🗺️  Testing Geocoding API...")
    print("-" * 60)

    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": "London", "limit": 5, "appid": api_key}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if data:
                    print(f"✅ Geocoding API works!")
                    print(f"   Found {len(data)} result(s) for 'London':")
                    for result in data[:3]:
                        print(f"   • {result['name']}, {result.get('state', '')}, {result['country']}")
                    return True
                else:
                    print(f"⚠️  Geocoding API returned empty results")
                    print(f"   This is unusual for 'London'")
                    return False
            elif response.status_code == 401:
                print(f"❌ Geocoding API: Invalid API key (401)")
                print(f"   Your API key doesn't have access to geocoding")
                return False
            else:
                print(f"❌ Geocoding API failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Geocoding API error: {e}")
        return False


async def test_specific_location(api_key: str, location: str):
    """Test geocoding a specific location."""
    print(f"\n📍 Testing location: '{location}'...")
    print("-" * 60)

    # Normalize country codes
    country_code_map = {
        "UK": "GB",
        "USA": "US",
        "United States": "US",
        "United Kingdom": "GB",
    }

    search_query = location
    for old_code, new_code in country_code_map.items():
        if old_code in search_query:
            search_query = search_query.replace(f", {old_code}", f", {new_code}")
            search_query = search_query.replace(f",{old_code}", f",{new_code}")
            print(f"   Normalized: '{location}' → '{search_query}'")

    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": search_query, "limit": 5, "appid": api_key}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if data:
                    print(f"✅ Found {len(data)} result(s):")
                    for result in data:
                        print(f"   • {result['name']}, {result.get('state', '')}, {result['country']}")
                        print(f"     Lat: {result['lat']}, Lon: {result['lon']}")
                    return True
                else:
                    # Try without country code
                    if "," in search_query:
                        city_only = search_query.split(",")[0].strip()
                        print(f"   Retrying with city only: '{city_only}'...")
                        params = {"q": city_only, "limit": 5, "appid": api_key}
                        response = await client.get(url, params=params)

                        if response.status_code == 200:
                            data = response.json()
                            if data:
                                print(f"✅ Found {len(data)} result(s):")
                                for result in data:
                                    print(f"   • {result['name']}, {result.get('state', '')}, {result['country']}")
                                    print(f"     Lat: {result['lat']}, Lon: {result['lon']}")
                                return True

                    print(f"❌ No results found for '{location}'")
                    return False
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    """Main diagnostic function."""
    print("\n" + "=" * 60)
    print("🔧 Tempura Diagnostic Tool")
    print("=" * 60)

    # Get API key
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        print("\n📝 Enter your OpenWeatherMap API key:")
        api_key = input("API Key: ").strip()

    if not api_key:
        print("❌ No API key provided!")
        return 1

    print(f"\n🔑 Testing API key: {api_key[:4]}...{api_key[-4:]}")
    print(f"   Length: {len(api_key)} characters (should be 32)")

    if len(api_key) != 32:
        print("⚠️  Warning: API key should be 32 characters long")

    # Run tests
    weather_ok = await test_weather_api(api_key)
    geocoding_ok = await test_geocoding_api(api_key)

    # Test specific locations if user wants
    if geocoding_ok:
        print("\n" + "=" * 60)
        test_location = input("Test a specific location? (press Enter to skip): ").strip()
        if test_location:
            await test_specific_location(api_key, test_location)

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Weather API:    {'✅ Working' if weather_ok else '❌ Failed'}")
    print(f"Geocoding API:  {'✅ Working' if geocoding_ok else '❌ Failed'}")
    print()

    if weather_ok and geocoding_ok:
        print("✅ All tests passed! Your API key is working correctly.")
        print("   You can use this key in Tempura.")
    elif weather_ok and not geocoding_ok:
        print("⚠️  Weather API works, but Geocoding API failed.")
        print()
        print("Possible issues:")
        print("1. New API keys take 10-15 minutes to activate geocoding")
        print("2. Free tier keys should have geocoding access")
        print("3. Check your subscription at: https://home.openweathermap.org/")
    else:
        print("❌ Tests failed. Check the errors above.")
        print()
        print("Common issues:")
        print("1. Wait 10-15 minutes if you just created the key")
        print("2. Check for typos in the API key")
        print("3. Verify the key at: https://home.openweathermap.org/api_keys")

    print("=" * 60 + "\n")

    return 0 if (weather_ok and geocoding_ok) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
