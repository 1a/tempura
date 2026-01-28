#!/usr/bin/env python3
"""Test script to debug API key issues."""

import asyncio
import httpx
import sys


async def test_api_key(api_key: str):
    """Test an OpenWeatherMap API key."""
    print(f"\n🔍 Testing API key: {api_key[:8]}...{api_key[-4:]}")
    print("=" * 60)

    # Test URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": 37.7749,
        "lon": -122.4194,
        "appid": api_key,
        "units": "metric"
    }

    print(f"\n📡 Making request to: {url}")
    print(f"📍 Testing with San Francisco coordinates")
    print(f"🔑 API key length: {len(api_key)} characters")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print("\n⏳ Sending request...")
            response = await client.get(url, params=params)

            print(f"\n📊 Response status: {response.status_code}")

            if response.status_code == 200:
                print("✅ SUCCESS! Your API key works!")
                data = response.json()
                print(f"\n🌤️  Weather in {data['name']}:")
                print(f"   Temperature: {data['main']['temp']}°C")
                print(f"   Description: {data['weather'][0]['description']}")
                print("\n✨ Your API key is valid and ready to use!")
                return True

            elif response.status_code == 401:
                print("❌ ERROR: Invalid API key (401 Unauthorized)")
                error_data = response.json()
                print(f"\n📝 Error message: {error_data.get('message', 'Unknown')}")
                print("\n💡 Possible issues:")
                print("   1. Wait 10-15 minutes if you just created the key")
                print("   2. Check for extra spaces or characters")
                print("   3. Make sure you copied the entire key")
                print("   4. Verify at: https://home.openweathermap.org/api_keys")
                return False

            elif response.status_code == 429:
                print("⚠️  ERROR: Rate limit exceeded (429)")
                print("   Wait a minute and try again")
                return False

            else:
                print(f"❌ ERROR: Unexpected status code {response.status_code}")
                print(f"\n📝 Response: {response.text}")
                return False

    except httpx.RequestError as e:
        print(f"❌ NETWORK ERROR: {e}")
        print("\n💡 Check your internet connection")
        return False

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False


async def main():
    """Main function."""
    print("\n" + "=" * 60)
    print("🌤️  OpenWeatherMap API Key Tester")
    print("=" * 60)

    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        print("\n📝 Please enter your OpenWeatherMap API key:")
        api_key = input("API Key: ").strip()

    if not api_key:
        print("❌ No API key provided!")
        sys.exit(1)

    success = await test_api_key(api_key)

    print("\n" + "=" * 60)
    if success:
        print("✅ Test passed! You can use this key in Tempura.")
    else:
        print("❌ Test failed. See the error details above.")
    print("=" * 60 + "\n")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
