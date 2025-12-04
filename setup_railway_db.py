#!/usr/bin/env python3
"""
Direct Railway PostgreSQL population script
This script connects directly to Railway's PostgreSQL and populates it with data
"""
import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

def get_railway_db_url():
    """Get Railway DATABASE_URL from environment or prompt user"""
    db_url = os.environ.get('DATABASE_URL')

    if not db_url:
        print("🔍 DATABASE_URL not found in environment.")
        print("📋 Get your DATABASE_URL from Railway Dashboard:")
        print("   1. Go to your Railway PostgreSQL service")
        print("   2. Click 'Connect' tab")
        print("   3. Copy the 'DATABASE_URL' value")
        print("")
        db_url = input("Paste your DATABASE_URL here: ").strip()

    return db_url

def create_tables_and_data(db_url):
    """Create tables and populate with sample data"""

    try:
        # Connect to Railway PostgreSQL
        print("🔌 Connecting to Railway PostgreSQL...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        print("✅ Connected successfully!")

        # Create tables SQL
        create_tables_sql = """
        -- Create pokemon_v2_type table
        CREATE TABLE IF NOT EXISTS pokemon_v2_type (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        
        -- Create pokemon_v2_ability table  
        CREATE TABLE IF NOT EXISTS pokemon_v2_ability (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        
        -- Create pokemon_v2_pokemon table
        CREATE TABLE IF NOT EXISTS pokemon_v2_pokemon (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            height INTEGER,
            weight INTEGER,
            base_experience INTEGER
        );
        
        -- Create pokemon_v2_berry table
        CREATE TABLE IF NOT EXISTS pokemon_v2_berry (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            growth_time INTEGER,
            max_harvest INTEGER,
            size INTEGER
        );
        """

        print("📊 Creating tables...")
        cur.execute(create_tables_sql)

        # Insert sample data
        print("🎓 Inserting educational sample data...")

        # Insert types
        types_data = [
            (1, 'grass'), (2, 'poison'), (3, 'fire'),
            (4, 'water'), (5, 'electric'), (6, 'psychic')
        ]

        cur.execute("DELETE FROM pokemon_v2_type")  # Clear existing
        for type_id, name in types_data:
            cur.execute(
                "INSERT INTO pokemon_v2_type (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                (type_id, name)
            )

        # Insert abilities
        abilities_data = [
            (1, 'overgrow'), (2, 'chlorophyll'), (3, 'blaze'), (4, 'solar-power'),
            (5, 'torrent'), (6, 'rain-dish'), (7, 'static'), (8, 'lightning-rod')
        ]

        cur.execute("DELETE FROM pokemon_v2_ability")  # Clear existing
        for ability_id, name in abilities_data:
            cur.execute(
                "INSERT INTO pokemon_v2_ability (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                (ability_id, name)
            )

        # Insert Pokemon
        pokemon_data = [
            (1, 'bulbasaur', 7, 69, 64),
            (4, 'charmander', 6, 85, 62),
            (7, 'squirtle', 5, 90, 63),
            (25, 'pikachu', 4, 60, 112),
            (150, 'mewtwo', 20, 1220, 340)
        ]

        cur.execute("DELETE FROM pokemon_v2_pokemon")  # Clear existing
        for poke_id, name, height, weight, base_exp in pokemon_data:
            cur.execute(
                "INSERT INTO pokemon_v2_pokemon (id, name, height, weight, base_experience) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (poke_id, name, height, weight, base_exp)
            )

        # Insert berries
        berries_data = [
            (1, 'cheri', 3, 5, 20),
            (2, 'chesto', 3, 5, 80),
            (3, 'pecha', 3, 5, 40),
            (4, 'rawst', 3, 5, 32),
            (5, 'aspear', 3, 5, 50)
        ]

        cur.execute("DELETE FROM pokemon_v2_berry")  # Clear existing
        for berry_id, name, growth_time, max_harvest, size in berries_data:
            cur.execute(
                "INSERT INTO pokemon_v2_berry (id, name, growth_time, max_harvest, size) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (berry_id, name, growth_time, max_harvest, size)
            )

        # Commit changes
        conn.commit()

        # Verify data
        print("\n📊 Verifying data...")

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_pokemon")
        pokemon_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_ability")
        ability_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_type")
        type_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_berry")
        berry_count = cur.fetchone()[0]

        print(f"✅ Data loaded successfully!")
        print(f"   Pokemon: {pokemon_count}")
        print(f"   Abilities: {ability_count}")
        print(f"   Types: {type_count}")
        print(f"   Berries: {berry_count}")

        # Show sample data
        print(f"\n🐾 Sample Pokemon:")
        cur.execute("SELECT name, height, weight FROM pokemon_v2_pokemon LIMIT 3")
        for row in cur.fetchall():
            print(f"   - {row['name']}: height={row['height']}, weight={row['weight']}")

        cur.close()
        conn.close()

        print(f"\n🎉 Railway PostgreSQL setup complete!")
        print(f"🔗 Your educational API endpoints should now work:")
        print(f"   https://your-app.railway.app/api/v2/writable-pokemon/")
        print(f"   https://your-app.railway.app/api/v2/writable-ability/")
        print(f"   https://your-app.railway.app/api/v2/writable-type/")
        print(f"   https://your-app.railway.app/api/v2/writable-berry/")

    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        print(f"💡 Make sure your DATABASE_URL is correct")
        print(f"💡 Check that your Railway PostgreSQL service is running")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚂 Railway PostgreSQL Direct Setup")
    print("=" * 50)
    print("This script will directly populate your Railway PostgreSQL database")
    print("with sample data for your educational Pokemon API.\n")

    # Get DATABASE_URL
    db_url = get_railway_db_url()

    if not db_url:
        print("❌ No DATABASE_URL provided. Exiting.")
        return

    # Validate URL format
    if not db_url.startswith('postgresql://'):
        print("❌ Invalid DATABASE_URL format. Should start with postgresql://")
        return

    print(f"🎯 Using DATABASE_URL: {db_url[:20]}...{db_url[-20:]}")

    # Create tables and populate data
    create_tables_and_data(db_url)

if __name__ == "__main__":
    main()
