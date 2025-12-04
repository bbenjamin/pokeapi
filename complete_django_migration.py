#!/usr/bin/env python3
"""
Complete Django Migration + Data Restoration
This approach:
1. Runs proper Django migrations to create complete schema
2. Restores your existing data
3. Ensures all relationships work correctly
"""

import os
import subprocess
import psycopg2

# Get Railway database URL from environment variable
RAILWAY_DB_URL = os.environ.get('DATABASE_URL')

if not RAILWAY_DB_URL:
    print("❌ DATABASE_URL environment variable not set!")
    print("💡 Set it with: export DATABASE_URL='your-railway-database-url'")
    exit(1)

def backup_existing_data():
    """Backup current data before schema recreation"""
    print("📦 Backing up existing data...")

    try:
        conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = conn.cursor()

        # Backup key tables
        backup_queries = {
            'berries': "SELECT * FROM pokemon_v2_berry",
            'pokemon': "SELECT * FROM pokemon_v2_pokemon",
            'abilities': "SELECT * FROM pokemon_v2_ability",
            'types': "SELECT * FROM pokemon_v2_type",
            'berry_flavors': "SELECT * FROM pokemon_v2_berryflavor",
            'berry_flavor_map': "SELECT * FROM pokemon_v2_berryflavormap"
        }

        backed_up_data = {}

        for table_name, query in backup_queries.items():
            try:
                cur.execute(query)
                backed_up_data[table_name] = cur.fetchall()
                cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = 'pokemon_v2_{table_name.replace('_', '')}' ORDER BY ordinal_position")
                backed_up_data[f"{table_name}_columns"] = [row[0] for row in cur.fetchall()]
                print(f"   ✅ Backed up {table_name}: {len(backed_up_data[table_name])} records")
            except Exception as e:
                print(f"   ⚠️ Could not backup {table_name}: {e}")
                backed_up_data[table_name] = []

        cur.close()
        conn.close()

        return backed_up_data

    except Exception as e:
        print(f"   ❌ Backup failed: {e}")
        return {}

def run_django_migrations():
    """Run proper Django migrations to create complete schema"""
    print("🔧 Running Django migrations to create proper schema...")

    try:
        # Set environment for Railway
        env = os.environ.copy()
        env['DATABASE_URL'] = RAILWAY_DB_URL
        env['RAILWAY_ENVIRONMENT'] = 'production'

        # Run migrations
        result = subprocess.run(
            ['python', 'manage.py', 'migrate', '--run-syncdb'],
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode == 0:
            print("   ✅ Django migrations completed successfully!")
            return True
        else:
            print(f"   ❌ Migrations failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"   ❌ Migration error: {e}")
        return False

def restore_data(backed_up_data):
    """Restore backed up data to new schema"""
    print("📥 Restoring data to new schema...")

    try:
        conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = conn.cursor()

        # Restore data in dependency order
        restore_order = ['types', 'abilities', 'berries', 'pokemon', 'berry_flavors', 'berry_flavor_map']

        for table_name in restore_order:
            if table_name in backed_up_data and backed_up_data[table_name]:
                data = backed_up_data[table_name]
                columns = backed_up_data.get(f"{table_name}_columns", [])

                if not columns:
                    continue

                # Build insert statement
                db_table_name = f"pokemon_v2_{table_name.replace('_', '')}"
                placeholders = ', '.join(['%s'] * len(columns))
                insert_sql = f"INSERT INTO {db_table_name} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING"

                # Insert data
                for row in data:
                    try:
                        cur.execute(insert_sql, row)
                    except Exception as e:
                        print(f"   ⚠️ Could not insert row in {table_name}: {e}")

                conn.commit()
                print(f"   ✅ Restored {table_name}: {len(data)} records")

        cur.close()
        conn.close()

        return True

    except Exception as e:
        print(f"   ❌ Data restoration failed: {e}")
        return False

def test_endpoints():
    """Test that endpoints work after migration"""
    print("🧪 Testing endpoints after migration...")

    import urllib.request
    import json

    endpoints = [
        ('Berry List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/'),
        ('Berry Detail', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/'),
        ('Pokemon List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-pokemon/'),
        ('Type List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-type/')
    ]

    all_working = True

    for name, url in endpoints:
        try:
            response = urllib.request.urlopen(url, timeout=15)
            if response.getcode() == 200:
                data = json.loads(response.read())
                if 'results' in data or 'name' in data:
                    print(f"   ✅ {name}: Working")
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
    print("🔄 Complete Django Schema Migration with Data Preservation")
    print("=" * 70)
    print("This will create a complete Django schema and restore your data\n")

    # Step 1: Backup existing data
    backed_up_data = backup_existing_data()
    if not backed_up_data:
        print("❌ Could not backup data. Aborting for safety.")
        return False

    # Step 2: Run Django migrations
    print(f"\n🔧 Creating proper Django schema...")
    if not run_django_migrations():
        print("❌ Could not run Django migrations.")
        return False

    # Step 3: Restore data
    print(f"\n📥 Restoring your data...")
    if not restore_data(backed_up_data):
        print("❌ Could not restore data.")
        return False

    # Step 4: Test endpoints
    print(f"\n🧪 Testing endpoints...")
    if test_endpoints():
        print("\n🎉 Complete migration successful!")
        print("🚂 Your educational Pokemon API is now fully functional!")
        return True
    else:
        print("\n⚠️ Migration completed but some endpoints have issues.")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'✅ Success!' if success else '❌ Failed!'}")
    exit(0 if success else 1)
