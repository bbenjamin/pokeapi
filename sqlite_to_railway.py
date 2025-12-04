#!/usr/bin/env python3
"""
Force SQLite Export and Railway Import
This script temporarily configures Django to use SQLite and exports the data
"""

import os
import sys
import django
from django.conf import settings

# Force Django to use SQLite database
os.environ['FORCE_SQLITE'] = 'true'

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def export_sqlite_data():
    """Export data from SQLite database"""

    # Temporarily override database settings to use SQLite
    original_databases = settings.DATABASES.copy()

    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/Users/ben.mullins/source/pokeapi/db.sqlite3',
        }
    }

    print("📤 Exporting data from local SQLite database...")

    try:
        # Import Django management
        from django.core.management import execute_from_command_line

        # Export data
        execute_from_command_line(['manage.py', 'dumpdata', 'pokemon_v2', '--indent=2', '--output=sqlite_export.json'])

        # Check if export was successful
        if os.path.exists('sqlite_export.json') and os.path.getsize('sqlite_export.json') > 100:
            print("   ✅ SQLite export successful!")

            # Check what we exported
            import json
            with open('sqlite_export.json', 'r') as f:
                data = json.load(f)

            print(f"   📊 Exported {len(data)} objects")

            # Show summary by model
            from collections import Counter
            model_counts = Counter(item['model'] for item in data)
            for model, count in model_counts.items():
                print(f"     - {model}: {count}")

            return 'sqlite_export.json'
        else:
            print("   ❌ SQLite export failed or empty")
            return None

    except Exception as e:
        print(f"   ❌ Export error: {e}")
        return None
    finally:
        # Restore original database settings
        settings.DATABASES = original_databases

def import_to_railway(export_file):
    """Import data to Railway database"""
    print("📥 Importing data to Railway PostgreSQL...")

    try:
        # Set Railway DATABASE_URL
        os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', input("Enter your Railway DATABASE_URL: ").strip())
        os.environ['RAILWAY_ENVIRONMENT'] = 'production'

        # Force Django to reconfigure with Railway settings
        from django.core.management import execute_from_command_line

        # First run migrations to create tables
        print("   🔧 Running migrations on Railway...")
        execute_from_command_line(['manage.py', 'migrate'])

        # Then load data
        print("   📥 Loading data to Railway...")
        execute_from_command_line(['manage.py', 'loaddata', export_file])

        print("   ✅ Railway import successful!")
        return True

    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_endpoints():
    """Test Railway endpoints"""
    print("🧪 Testing Railway endpoints...")

    import urllib.request
    import json

    endpoints = [
        ('Berry List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/'),
        ('Berry Detail', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/'),
        ('Pokemon List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-pokemon/'),
        ('Abilities List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-ability/')
    ]

    all_working = True

    for name, url in endpoints:
        try:
            response = urllib.request.urlopen(url, timeout=15)
            if response.getcode() == 200:
                data = json.loads(response.read())
                if 'results' in data or 'name' in data:
                    print(f"   ✅ {name}: Working ({data.get('count', 'detail')} items)")
                else:
                    print(f"   ⚠️ {name}: Unexpected response format")
                    all_working = False
            else:
                print(f"   ❌ {name}: HTTP {response.getcode()}")
                all_working = False
        except Exception as e:
            print(f"   ❌ {name}: {str(e)[:50]}...")
            all_working = False

    return all_working

def main():
    print("🔄 SQLite → Railway Database Migration")
    print("=" * 50)
    print("Exporting from local SQLite and importing to Railway PostgreSQL\n")

    # Initialize Django
    django.setup()

    # Step 1: Export SQLite data
    export_file = export_sqlite_data()
    if not export_file:
        print("\n❌ Could not export SQLite data.")
        return False

    # Step 2: Import to Railway
    print(f"\n🚂 Importing to Railway...")
    if not import_to_railway(export_file):
        print("\n❌ Could not import to Railway.")
        return False

    # Step 3: Test endpoints
    print(f"\n🧪 Testing endpoints...")
    if test_endpoints():
        print("\n🎉 Migration completed successfully!")
        print("🚂 Your Railway database now has complete working data!")

        # Clean up
        try:
            os.remove(export_file)
            print(f"🧹 Cleaned up: {export_file}")
        except:
            pass

        print(f"\n🔗 Your educational API is ready:")
        print(f"   Berry Detail: https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/")
        print(f"   Interactive Docs: https://pokeapi-production-2219.up.railway.app/api/v2/schema/swagger-ui/")

        return True
    else:
        print("\n⚠️ Migration completed but some endpoints have issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
