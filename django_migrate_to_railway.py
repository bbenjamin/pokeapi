#!/usr/bin/env python3
"""
Django-based Local to Railway Database Migration
Uses Django's dumpdata/loaddata commands for safer migration
"""

import subprocess
import os
import json

def export_django_data():
    """Export Django data using dumpdata command"""
    print("📤 Exporting Django data using dumpdata...")

    try:
        # Export all pokemon_v2 data
        dump_file = "pokemon_v2_data.json"

        cmd = f"python manage.py dumpdata pokemon_v2 --indent 2 > {dump_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0 and os.path.exists(dump_file):
            # Check if file has content
            with open(dump_file, 'r') as f:
                data = json.load(f)

            if data:
                print(f"   ✅ Exported {len(data)} objects to {dump_file}")
                return dump_file
            else:
                print("   ❌ Export file is empty")
                return None
        else:
            print(f"   ❌ Export failed: {result.stderr}")
            return None

    except Exception as e:
        print(f"   ❌ Export error: {e}")
        return None

def setup_railway_for_import():
    """Prepare Railway database for data import"""
    print("🔧 Setting up Railway database for import...")

    try:
        # Run migrations on Railway to create tables
        cmd = "python manage.py migrate --settings=config.settings"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              env={**os.environ, 'DATABASE_URL': os.environ.get('DATABASE_URL', '')})

        if result.returncode == 0:
            print("   ✅ Migrations completed on Railway")
            return True
        else:
            print(f"   ❌ Migration failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"   ❌ Migration setup error: {e}")
        return False

def import_django_data(dump_file):
    """Import Django data using loaddata command"""
    print(f"📥 Importing {dump_file} to Railway...")

    try:
        cmd = f"python manage.py loaddata {dump_file} --settings=config.settings"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              env={**os.environ, 'DATABASE_URL': os.environ.get('DATABASE_URL', '')})

        if result.returncode == 0:
            print("   ✅ Data import successful!")
            return True
        else:
            print(f"   ❌ Import failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_railway_endpoints():
    """Test Railway endpoints to verify migration"""
    print("🧪 Testing Railway endpoints...")

    endpoints = [
        "https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/",
        "https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/",
        "https://pokeapi-production-2219.up.railway.app/api/v2/writable-pokemon/",
        "https://pokeapi-production-2219.up.railway.app/api/v2/writable-ability/"
    ]

    import urllib.request
    import urllib.error

    all_working = True

    for endpoint in endpoints:
        try:
            response = urllib.request.urlopen(endpoint, timeout=10)
            if response.getcode() == 200:
                print(f"   ✅ {endpoint.split('/')[-2]}: Working")
            else:
                print(f"   ❌ {endpoint.split('/')[-2]}: HTTP {response.getcode()}")
                all_working = False
        except Exception as e:
            print(f"   ❌ {endpoint.split('/')[-2]}: {str(e)[:50]}...")
            all_working = False

    return all_working

def main():
    print("🔄 Django Local → Railway Database Migration")
    print("=" * 50)
    print("This uses Django's dumpdata/loaddata for safe migration\n")

    # Check if we're in a Django project
    if not os.path.exists('manage.py'):
        print("❌ No manage.py found. Please run this from your Django project root.")
        return False

    # Step 1: Export local Django data
    dump_file = export_django_data()
    if not dump_file:
        print("\n❌ Could not export local Django data.")
        print("💡 Make sure you have data in your local database:")
        print("   python manage.py migrate")
        print("   python manage.py loaddata some_data.json")
        return False

    # Step 2: Setup Railway database
    print(f"\n🚂 Setting up Railway database...")
    if not setup_railway_for_import():
        print("\n❌ Could not setup Railway database for import.")
        return False

    # Step 3: Import data to Railway
    print(f"\n📥 Importing data to Railway...")
    if not import_django_data(dump_file):
        print("\n❌ Could not import data to Railway.")
        return False

    # Step 4: Test endpoints
    print(f"\n🧪 Testing Railway endpoints...")
    if test_railway_endpoints():
        print("\n🎉 Migration completed successfully!")
        print("🚂 Your Railway database now has complete working data!")

        # Clean up
        try:
            os.remove(dump_file)
            print(f"🧹 Cleaned up: {dump_file}")
        except:
            pass

        print(f"\n🔗 Your educational API is ready:")
        print(f"   Berry List: https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")
        print(f"   Berry Detail: https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/")
        print(f"   Interactive Docs: https://pokeapi-production-2219.up.railway.app/api/v2/schema/swagger-ui/")

        return True
    else:
        print("\n⚠️ Migration completed but some endpoints are not working.")
        print("💡 Check Railway logs for detailed error information.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
