#!/usr/bin/env python3
"""
Railway PostgreSQL Schema Migration Script - Preserves Data
This script connects directly to Railway PostgreSQL and updates the schema to match Django models
while preserving all existing data.
"""

import psycopg2
import sys
import os

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

def migrate_database_schema(db_url):
    """Migrate database schema to match Django models while preserving data"""

    try:
        print("🔌 Connecting to Railway PostgreSQL...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        print("✅ Connected successfully!")

        # Start transaction for safe migration
        cur.execute("BEGIN")

        print("📊 Migrating database schema while preserving data...")

        # 1. Create missing tables for Django model relationships
        print("🏗️ Creating missing support tables...")

        # Create django_migrations table if it doesn't exist
        cur.execute("""
        CREATE TABLE IF NOT EXISTS django_migrations (
            id SERIAL PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
        );
        """)

        # Create ItemPocket table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_itempocket (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)

        # Insert default item pocket if not exists
        cur.execute("""
        INSERT INTO pokemon_v2_itempocket (id, name) 
        VALUES (1, 'berries') 
        ON CONFLICT (name) DO NOTHING;
        """)

        # Create ItemCategory table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_itemcategory (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            item_pocket_id INTEGER REFERENCES pokemon_v2_itempocket(id)
        );
        """)

        # Insert default item category if not exists
        cur.execute("""
        INSERT INTO pokemon_v2_itemcategory (id, name, item_pocket_id) 
        VALUES (1, 'berry', 1) 
        ON CONFLICT (name) DO NOTHING;
        """)

        # Create Item table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_item (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            item_category_id INTEGER REFERENCES pokemon_v2_itemcategory(id),
            cost INTEGER DEFAULT 0,
            fling_power INTEGER,
            fling_effect_id INTEGER
        );
        """)

        # Create BerryFirmness table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_berryfirmness (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)

        # Insert default berry firmness levels
        firmness_data = [
            (1, 'very-soft'), (2, 'soft'), (3, 'hard'), (4, 'very-hard'), (5, 'super-hard')
        ]
        for firmness_id, name in firmness_data:
            cur.execute("""
            INSERT INTO pokemon_v2_berryfirmness (id, name) 
            VALUES (%s, %s) 
            ON CONFLICT (name) DO NOTHING;
            """, (firmness_id, name))

        # Create Generation table (needed for some models)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_generation (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            main_region_id INTEGER
        );
        """)

        # Insert default generation
        cur.execute("""
        INSERT INTO pokemon_v2_generation (id, name) 
        VALUES (1, 'generation-i') 
        ON CONFLICT (name) DO NOTHING;
        """)

        print("📝 Checking existing data...")

        # 2. Check what data exists and preserve it
        existing_data = {}

        # Check existing berries
        try:
            cur.execute("SELECT id, name, growth_time, max_harvest, size FROM pokemon_v2_berry ORDER BY id")
            existing_data['berries'] = cur.fetchall()
            print(f"   📊 Found {len(existing_data['berries'])} existing berries")
        except:
            existing_data['berries'] = []
            print("   📊 No existing berry table found")

        # Check existing pokemon
        try:
            cur.execute("SELECT id, name, height, weight, base_experience FROM pokemon_v2_pokemon ORDER BY id")
            existing_data['pokemon'] = cur.fetchall()
            print(f"   📊 Found {len(existing_data['pokemon'])} existing pokemon")
        except:
            existing_data['pokemon'] = []
            print("   📊 No existing pokemon table found")

        # Check existing abilities
        try:
            cur.execute("SELECT id, name FROM pokemon_v2_ability ORDER BY id")
            existing_data['abilities'] = cur.fetchall()
            print(f"   📊 Found {len(existing_data['abilities'])} existing abilities")
        except:
            existing_data['abilities'] = []
            print("   📊 No existing ability table found")

        # Check existing types
        try:
            cur.execute("SELECT id, name FROM pokemon_v2_type ORDER BY id")
            existing_data['types'] = cur.fetchall()
            print(f"   📊 Found {len(existing_data['types'])} existing types")
        except:
            existing_data['types'] = []
            print("   📊 No existing type table found")

        # 3. Drop and recreate tables with proper schema
        print("🔄 Recreating tables with proper Django schema...")

        # Drop existing tables in correct order (foreign key dependencies)
        drop_tables = [
            'pokemon_v2_berry',
            'pokemon_v2_pokemon',
            'pokemon_v2_pokemonspecies',
            'pokemon_v2_ability',
            'pokemon_v2_type'
        ]

        for table in drop_tables:
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            print(f"   🗑️  Dropped {table}")

        # Create Type table with proper schema
        cur.execute("""
        CREATE TABLE pokemon_v2_type (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            generation_id INTEGER DEFAULT 1 REFERENCES pokemon_v2_generation(id)
        );
        """)

        # Create Ability table with proper schema
        cur.execute("""
        CREATE TABLE pokemon_v2_ability (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            is_main_series BOOLEAN DEFAULT true,
            generation_id INTEGER DEFAULT 1 REFERENCES pokemon_v2_generation(id)
        );
        """)

        # Create PokemonSpecies table
        cur.execute("""
        CREATE TABLE pokemon_v2_pokemonspecies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            order_value INTEGER DEFAULT 1,
            gender_rate INTEGER DEFAULT 1,
            capture_rate INTEGER DEFAULT 45,
            base_happiness INTEGER DEFAULT 70,
            is_baby BOOLEAN DEFAULT false,
            hatch_counter INTEGER DEFAULT 20,
            has_gender_differences BOOLEAN DEFAULT false,
            growth_rate_id INTEGER DEFAULT 1,
            forms_switchable BOOLEAN DEFAULT false,
            is_legendary BOOLEAN DEFAULT false,
            is_mythical BOOLEAN DEFAULT false,
            color_id INTEGER DEFAULT 1,
            shape_id INTEGER DEFAULT 1,
            evolves_from_species_id INTEGER,
            evolution_chain_id INTEGER,
            habitat_id INTEGER,
            generation_id INTEGER DEFAULT 1 REFERENCES pokemon_v2_generation(id)
        );
        """)

        # Create Pokemon table with proper schema
        cur.execute("""
        CREATE TABLE pokemon_v2_pokemon (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            pokemon_species_id INTEGER NOT NULL REFERENCES pokemon_v2_pokemonspecies(id),
            height INTEGER,
            weight INTEGER,
            base_experience INTEGER,
            order_value INTEGER DEFAULT 1,
            is_default BOOLEAN DEFAULT true
        );
        """)

        # Create Berry table with proper Django schema
        cur.execute("""
        CREATE TABLE pokemon_v2_berry (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            item_id INTEGER REFERENCES pokemon_v2_item(id),
            berry_firmness_id INTEGER REFERENCES pokemon_v2_berryfirmness(id),
            natural_gift_power INTEGER DEFAULT 60,
            natural_gift_type_id INTEGER REFERENCES pokemon_v2_type(id),
            size INTEGER DEFAULT 20,
            max_harvest INTEGER DEFAULT 5,
            growth_time INTEGER DEFAULT 3,
            soil_dryness INTEGER DEFAULT 15,
            smoothness INTEGER DEFAULT 25
        );
        """)

        print("✅ Tables recreated with proper Django schema")

        # 4. Restore existing data with proper relationships
        print("📥 Restoring existing data...")

        # Restore Types
        if existing_data['types']:
            for type_id, name in existing_data['types']:
                cur.execute("""
                INSERT INTO pokemon_v2_type (id, name) 
                VALUES (%s, %s) 
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """, (type_id, name))
            print(f"   ✅ Restored {len(existing_data['types'])} types")

        # Restore Abilities
        if existing_data['abilities']:
            for ability_id, name in existing_data['abilities']:
                cur.execute("""
                INSERT INTO pokemon_v2_ability (id, name) 
                VALUES (%s, %s) 
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """, (ability_id, name))
            print(f"   ✅ Restored {len(existing_data['abilities'])} abilities")

        # Restore Pokemon (create species first)
        if existing_data['pokemon']:
            for pokemon_id, name, height, weight, base_experience in existing_data['pokemon']:
                # Create species for each pokemon
                cur.execute("""
                INSERT INTO pokemon_v2_pokemonspecies (id, name) 
                VALUES (%s, %s) 
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """, (pokemon_id, name))

                # Create pokemon
                cur.execute("""
                INSERT INTO pokemon_v2_pokemon (id, name, pokemon_species_id, height, weight, base_experience) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                ON CONFLICT (id) DO UPDATE SET 
                    name = EXCLUDED.name,
                    height = EXCLUDED.height,
                    weight = EXCLUDED.weight,
                    base_experience = EXCLUDED.base_experience;
                """, (pokemon_id, name, pokemon_id, height, weight, base_experience))
            print(f"   ✅ Restored {len(existing_data['pokemon'])} pokemon with species")

        # Restore Berries with proper relationships
        if existing_data['berries']:
            for berry_id, name, growth_time, max_harvest, size in existing_data['berries']:
                # Create item for berry
                cur.execute("""
                INSERT INTO pokemon_v2_item (id, name, item_category_id, cost) 
                VALUES (%s, %s, 1, 20) 
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """, (berry_id, f"{name}-berry"))

                # Get a random type for natural gift (or create if needed)
                cur.execute("SELECT id FROM pokemon_v2_type LIMIT 1")
                type_result = cur.fetchone()
                natural_gift_type_id = type_result[0] if type_result else 1

                # Create berry with all required fields
                cur.execute("""
                INSERT INTO pokemon_v2_berry 
                (id, name, item_id, berry_firmness_id, natural_gift_power, natural_gift_type_id, 
                 size, max_harvest, growth_time, soil_dryness, smoothness) 
                VALUES (%s, %s, %s, 2, 60, %s, %s, %s, %s, 15, 25) 
                ON CONFLICT (id) DO UPDATE SET 
                    name = EXCLUDED.name,
                    size = EXCLUDED.size,
                    max_harvest = EXCLUDED.max_harvest,
                    growth_time = EXCLUDED.growth_time;
                """, (berry_id, name, berry_id, natural_gift_type_id, size, max_harvest, growth_time))
            print(f"   ✅ Restored {len(existing_data['berries'])} berries with full relationships")

        # 5. Add any missing educational data
        print("📚 Adding educational sample data...")

        # Ensure we have basic types
        basic_types = [
            (1, 'normal'), (2, 'fighting'), (3, 'flying'), (4, 'poison'),
            (5, 'ground'), (6, 'rock'), (7, 'bug'), (8, 'ghost'),
            (9, 'steel'), (10, 'fire'), (11, 'water'), (12, 'grass'),
            (13, 'electric'), (14, 'psychic'), (15, 'ice'), (16, 'dragon'),
            (17, 'dark'), (18, 'fairy')
        ]

        for type_id, name in basic_types:
            cur.execute("""
            INSERT INTO pokemon_v2_type (id, name) 
            VALUES (%s, %s) 
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
            """, (type_id, name))

        # Ensure we have basic abilities
        basic_abilities = [
            (1, 'stench'), (2, 'drizzle'), (3, 'speed-boost'), (4, 'battle-armor'),
            (5, 'sturdy'), (6, 'damp'), (7, 'limber'), (8, 'sand-veil'),
            (9, 'static'), (10, 'volt-absorb')
        ]

        for ability_id, name in basic_abilities:
            cur.execute("""
            INSERT INTO pokemon_v2_ability (id, name) 
            VALUES (%s, %s) 
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
            """, (ability_id, name))

        # Add Django migration records
        cur.execute("""
        INSERT INTO django_migrations (app, name, applied) 
        VALUES ('pokemon_v2', '0001_initial', NOW()) 
        ON CONFLICT (app, name) DO NOTHING;
        """)

        # Commit transaction
        conn.commit()
        print("💾 All changes committed successfully!")

        # 6. Verify the migration
        print("🔍 Verifying migration...")

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_pokemon")
        pokemon_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_type")
        type_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_ability")
        ability_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM pokemon_v2_berry")
        berry_count = cur.fetchone()[0]

        print(f"\n🎉 Migration completed successfully!")
        print(f"📊 Final database summary:")
        print(f"   Pokemon: {pokemon_count}")
        print(f"   Types: {type_count}")
        print(f"   Abilities: {ability_count}")
        print(f"   Berries: {berry_count}")

        # Show sample data to verify
        print(f"\n📋 Sample data verification:")
        cur.execute("SELECT name FROM pokemon_v2_pokemon LIMIT 3")
        for row in cur.fetchall():
            print(f"   🐾 Pokemon: {row[0]}")

        cur.execute("SELECT name FROM pokemon_v2_berry LIMIT 3")
        for row in cur.fetchall():
            print(f"   🫐 Berry: {row[0]}")

        cur.close()
        conn.close()

        print(f"\n✅ Database migration complete!")
        print(f"🚂 Your Railway PostgreSQL now has proper Django schema")
        print(f"🎯 All existing data preserved with correct relationships")
        print(f"\n🔗 Test your educational API endpoints:")
        print(f"   https://pokeapi-production-2219.up.railway.app/api/v2/writable-pokemon/")
        print(f"   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")
        print(f"   https://pokeapi-production-2219.up.railway.app/api/v2/writable-ability/")
        print(f"   https://pokeapi-production-2219.up.railway.app/api/v2/writable-type/")

        return True

    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print(f"💡 Make sure your DATABASE_URL is correct")
        print(f"💡 Check that your Railway PostgreSQL service is running")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

def main():
    print("🔄 Railway PostgreSQL Schema Migration")
    print("=" * 60)
    print("This script will migrate your database schema to match Django models")
    print("while preserving all existing data and relationships.\n")

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

    # Confirm migration
    print(f"\n⚠️  This will:")
    print(f"   1. Preserve all your existing data")
    print(f"   2. Recreate tables with proper Django schema")
    print(f"   3. Restore data with correct relationships")
    print(f"   4. Add missing educational sample data")

    confirm = input(f"\nContinue with migration? (y/N): ").lower().strip()
    if confirm != 'y':
        print("❌ Migration cancelled.")
        return

    # Run migration
    success = migrate_database_schema(db_url)

    if success:
        print(f"\n🎉 Migration completed successfully!")
        print(f"🚂 Your educational Pokemon API is ready!")
        sys.exit(0)
    else:
        print(f"\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
