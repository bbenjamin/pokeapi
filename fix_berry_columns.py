#!/usr/bin/env python3
"""
Railway PostgreSQL Column Addition - Minimal Migration
Adds missing columns to existing tables without dropping data
"""

import psycopg2
import sys

def add_missing_columns(db_url):
    """Add missing columns to existing tables"""

    try:
        print("🔌 Connecting to Railway PostgreSQL...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        print("✅ Connected successfully!")
        print("📊 Checking current database structure...")

        # Check current berry table structure
        cur.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'pokemon_v2_berry' 
        ORDER BY ordinal_position;
        """)

        existing_columns = {row[0]: {'type': row[1], 'nullable': row[2]} for row in cur.fetchall()}
        print(f"   📋 Current berry columns: {list(existing_columns.keys())}")

        # Start transaction
        cur.execute("BEGIN")

        print("🏗️ Creating required support tables...")

        # Create BerryFirmness table if not exists
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_berryfirmness (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)

        # Insert firmness data only if table is empty
        cur.execute("SELECT COUNT(*) FROM pokemon_v2_berryfirmness")
        if cur.fetchone()[0] == 0:
            firmness_data = [
                (1, 'very-soft'), (2, 'soft'), (3, 'hard'), (4, 'very-hard'), (5, 'super-hard')
            ]
            for firmness_id, name in firmness_data:
                cur.execute("INSERT INTO pokemon_v2_berryfirmness (id, name) VALUES (%s, %s)", (firmness_id, name))
            print("   ✅ Added berry firmness data")

        # Create ItemPocket table if not exists
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_itempocket (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)

        # Insert item pocket only if not exists
        cur.execute("SELECT COUNT(*) FROM pokemon_v2_itempocket WHERE id = 1")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO pokemon_v2_itempocket (id, name) VALUES (1, 'berries')")
            print("   ✅ Added item pocket")

        # Create ItemCategory table if not exists
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_itemcategory (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            item_pocket_id INTEGER REFERENCES pokemon_v2_itempocket(id)
        );
        """)

        # Insert item category only if not exists
        cur.execute("SELECT COUNT(*) FROM pokemon_v2_itemcategory WHERE id = 1")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO pokemon_v2_itemcategory (id, name, item_pocket_id) VALUES (1, 'berry', 1)")
            print("   ✅ Added item category")

        # Create Item table if not exists
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

        print("📝 Adding missing columns to berry table...")

        # Define required columns for Berry model
        required_columns = {
            'item_id': 'INTEGER REFERENCES pokemon_v2_item(id)',
            'berry_firmness_id': 'INTEGER REFERENCES pokemon_v2_berryfirmness(id)',
            'natural_gift_power': 'INTEGER DEFAULT 60',
            'natural_gift_type_id': 'INTEGER REFERENCES pokemon_v2_type(id)',
            'soil_dryness': 'INTEGER DEFAULT 15',
            'smoothness': 'INTEGER DEFAULT 25'
        }

        # Add missing columns one by one
        for column_name, column_def in required_columns.items():
            if column_name not in existing_columns:
                try:
                    cur.execute(f"ALTER TABLE pokemon_v2_berry ADD COLUMN {column_name} {column_def}")
                    print(f"   ✅ Added column: {column_name}")
                except Exception as e:
                    print(f"   ⚠️  Could not add {column_name}: {e}")
            else:
                print(f"   ℹ️  Column {column_name} already exists")

        print("🔗 Creating items and relationships for existing berries...")

        # Get berries that need items created
        cur.execute("SELECT id, name FROM pokemon_v2_berry WHERE item_id IS NULL")
        berries_needing_items = cur.fetchall()

        for berry_id, berry_name in berries_needing_items:
            # Create item for this berry
            item_name = f"{berry_name}-berry"
            try:
                cur.execute("""
                INSERT INTO pokemon_v2_item (id, name, item_category_id, cost) 
                VALUES (%s, %s, 1, 20)
                """, (berry_id, item_name))
                print(f"   ✅ Created item: {item_name}")
            except psycopg2.errors.UniqueViolation:
                # Item already exists, that's fine
                pass
            except Exception as e:
                print(f"   ⚠️  Could not create item for {berry_name}: {e}")

        # Update berries with default relationships
        cur.execute("""
        UPDATE pokemon_v2_berry SET 
            item_id = COALESCE(item_id, id),
            berry_firmness_id = COALESCE(berry_firmness_id, 2),
            natural_gift_power = COALESCE(natural_gift_power, 60),
            natural_gift_type_id = COALESCE(natural_gift_type_id, 
                (SELECT id FROM pokemon_v2_type WHERE name = 'fire' LIMIT 1)),
            soil_dryness = COALESCE(soil_dryness, 15),
            smoothness = COALESCE(smoothness, 25)
        WHERE item_id IS NULL OR berry_firmness_id IS NULL;
        """)

        updated_rows = cur.rowcount
        if updated_rows > 0:
            print(f"   ✅ Updated {updated_rows} berries with relationships")

        # Commit all changes
        conn.commit()
        print("💾 All changes committed!")

        # Verify the berry table works
        print("🧪 Testing berry table...")
        cur.execute("""
        SELECT b.id, b.name, b.natural_gift_power, b.soil_dryness, b.smoothness,
               i.name as item_name, bf.name as firmness_name
        FROM pokemon_v2_berry b
        LEFT JOIN pokemon_v2_item i ON b.item_id = i.id  
        LEFT JOIN pokemon_v2_berryfirmness bf ON b.berry_firmness_id = bf.id
        LIMIT 3;
        """)

        test_berries = cur.fetchall()
        print("   📋 Sample berry data:")
        for row in test_berries:
            print(f"     🫐 {row[1]}: power={row[2]}, dryness={row[3]}, firmness={row[6]}")

        cur.close()
        conn.close()

        print(f"\n🎉 Berry table migration completed successfully!")
        print(f"🔗 Test your berry endpoint:")
        print(f"   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")

        return True

    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

def main():
    print("🔧 Railway Berry Table Column Migration")
    print("=" * 50)
    print("This script will add missing columns to your berry table")
    print("without dropping existing data.\n")

    # Get DATABASE_URL
    db_url = input("Paste your Railway DATABASE_URL: ").strip()

    if not db_url:
        print("❌ No DATABASE_URL provided. Exiting.")
        return

    if not db_url.startswith('postgresql://'):
        print("❌ Invalid DATABASE_URL format. Should start with postgresql://")
        return

    print(f"🎯 Using DATABASE_URL: {db_url[:20]}...{db_url[-20:]}")

    # Run migration
    success = add_missing_columns(db_url)

    if success:
        print(f"\n✅ Migration completed successfully!")
        print(f"🚂 Your berry endpoint should now work without column errors!")
        sys.exit(0)
    else:
        print(f"\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
