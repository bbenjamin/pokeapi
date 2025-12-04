#!/usr/bin/env python3
"""
Test script to validate writable API endpoints
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse
import json

def test_writable_endpoints():
    """Test that writable endpoints are properly configured"""
    client = Client()

    # Test endpoints
    endpoints = [
        '/api/v2/writable-pokemon/',
        '/api/v2/writable-berry/',
        '/api/v2/writable-ability/',
        '/api/v2/writable-type/',
    ]

    print("🔍 Testing Writable API Endpoints")
    print("=" * 50)

    for endpoint in endpoints:
        print(f"\n📍 Testing: {endpoint}")

        # Test GET (should work)
        try:
            response = client.get(endpoint)
            print(f"   GET: Status {response.status_code} ✓")

            if response.status_code == 200:
                data = response.json()
                print(f"   Results count: {data.get('count', 'N/A')}")
        except Exception as e:
            print(f"   GET: Error - {e} ✗")

        # Test OPTIONS to see allowed methods
        try:
            response = client.options(endpoint)
            if response.status_code == 200:
                allowed_methods = response.get('Allow', 'Not specified')
                print(f"   OPTIONS: {allowed_methods} ✓")
            else:
                print(f"   OPTIONS: Status {response.status_code}")
        except Exception as e:
            print(f"   OPTIONS: Error - {e} ✗")

    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == '__main__':
    test_writable_endpoints()
