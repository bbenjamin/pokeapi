#!/usr/bin/env python3
"""
Test script to demonstrate partial update functionality for educational endpoints
"""

import requests
import json

BASE_URL = "https://pokeapi-production-2219.up.railway.app/api/v2"

def test_partial_updates():
    """Test partial updates on writable endpoints"""

    print("🧪 Testing Partial Update Functionality")
    print("=" * 50)

    # Test Berry partial update
    print("\n🫐 Testing Berry Partial Update:")
    print("   URL: /writable-berry/1/")

    # Get current berry data
    berry_url = f"{BASE_URL}/writable-berry/1/"
    response = requests.get(berry_url)

    if response.status_code == 200:
        current_berry = response.json()
        print(f"   ✅ Current berry: {current_berry.get('name', 'Unknown')}")
        print(f"   📊 Current size: {current_berry.get('size', 'Unknown')}")

        # Test partial update - only change size
        update_data = {
            "size": 25  # Only updating size, keeping all other fields
        }

        print(f"\n   🔄 Attempting partial update (size only): {update_data}")

        # Test PUT request with partial data
        put_response = requests.put(berry_url, json=update_data, headers={'Content-Type': 'application/json'})

        if put_response.status_code in [200, 201]:
            updated_berry = put_response.json()
            print(f"   ✅ PUT Success! Updated size: {updated_berry.get('size', 'Unknown')}")
            print(f"   ✅ Name preserved: {updated_berry.get('name', 'Unknown')}")
        else:
            print(f"   ❌ PUT Failed: {put_response.status_code}")
            print(f"   📄 Response: {put_response.text[:200]}...")

        # Test PATCH request with partial data
        patch_data = {
            "growth_time": 4  # Only updating growth_time
        }

        print(f"\n   🔄 Attempting PATCH update: {patch_data}")
        patch_response = requests.patch(berry_url, json=patch_data, headers={'Content-Type': 'application/json'})

        if patch_response.status_code in [200, 201]:
            patched_berry = patch_response.json()
            print(f"   ✅ PATCH Success! Updated growth_time: {patched_berry.get('growth_time', 'Unknown')}")
        else:
            print(f"   ❌ PATCH Failed: {patch_response.status_code}")
            print(f"   📄 Response: {patch_response.text[:200]}...")

    else:
        print(f"   ❌ Could not fetch berry data: {response.status_code}")

    # Test Pokemon partial update
    print("\n🐾 Testing Pokemon Partial Update:")
    print("   URL: /writable-pokemon/1/")

    pokemon_url = f"{BASE_URL}/writable-pokemon/1/"
    response = requests.get(pokemon_url)

    if response.status_code == 200:
        current_pokemon = response.json()
        print(f"   ✅ Current pokemon: {current_pokemon.get('name', 'Unknown')}")

        # Test partial update - only change weight
        update_data = {
            "weight": 75  # Only updating weight
        }

        print(f"   🔄 Attempting partial update (weight only): {update_data}")
        put_response = requests.put(pokemon_url, json=update_data, headers={'Content-Type': 'application/json'})

        if put_response.status_code in [200, 201]:
            updated_pokemon = put_response.json()
            print(f"   ✅ PUT Success! Updated weight: {updated_pokemon.get('weight', 'Unknown')}")
        else:
            print(f"   ❌ PUT Failed: {put_response.status_code}")
            print(f"   📄 Response: {put_response.text[:200]}...")

    else:
        print(f"   ❌ Could not fetch pokemon data: {response.status_code}")

    print(f"\n🎓 Educational API Testing Complete!")
    print(f"🔗 Test these URLs in your browser or Postman:")
    print(f"   PUT  {BASE_URL}/writable-berry/1/")
    print(f"   PATCH {BASE_URL}/writable-berry/1/")
    print(f"   PUT  {BASE_URL}/writable-pokemon/1/")
    print(f"   Interactive Docs: {BASE_URL.replace('/api/v2', '')}/api/v2/schema/swagger-ui/")

if __name__ == "__main__":
    try:
        test_partial_updates()
    except Exception as e:
        print(f"❌ Test error: {e}")
        print("💡 Make sure your Railway API is running and accessible")
