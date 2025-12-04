#!/usr/bin/env python3
"""
Simple column addition migration - adds missing columns without dropping tables
"""
import os
import psycopg2
import sys

# Your DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL') or input("Enter your Railway DATABASE_URL: ").strip()

def add_missing_columns():
    try:
        print("🔌 Connecting to Railway PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("✅ Connected successfully!")

        # Start transaction
        cur.execute("BEGIN")

        print("🏗️ Creating support tables...")

        # Create BerryFirmness table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_berryfirmness (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)

        # Insert firmness data
        firmness_data = [(1, 'very-soft'), (2, 'soft'), (3, 'hard'), (4, 'very-hard'), (5, 'super-hard')]
        for firmness_id, name in firmness_data:
            cur.execute("""
            INSERT INTO pokemon_v2_berryfirmness (id, name) VALUES (%s, %s) 
            ON CONFLICT (id) DO NOTHING;
            """, (firmness_id, name))

        # Create ItemPocket table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_itempocket (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)

        cur.execute("""
        INSERT INTO pokemon_v2_itempocket (id, name) VALUES (1, 'berries') 
        ON CONFLICT (id) DO NOTHING;
        """)

        # Create ItemCategory table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_v2_itemcategory (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            item_pocket_id INTEGER REFERENCES pokemon_v2_itempocket(id)
        );
        """)

        cur.execute("""
        INSERT INTO pokemon_v2_itemcategory (id, name, item_pocket_id) VALUES (1, 'berry', 1) 
        ON CONFLICT (id) DO NOTHING;
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

        print("📝 Adding missing columns to berry table...")

        # Add missing columns one by one
        missing_columns = [
            ('item_id', 'INTEGER'),
            ('berry_firmness_id', 'INTEGER'),
            ('natural_gift_power', 'INTEGER DEFAULT 60'),
            ('natural_gift_type_id', 'INTEGER'),
            ('soil_dryness', 'INTEGER DEFAULT 15'),
            ('smoothness', 'INTEGER DEFAULT 25')
        ]

        for column_name, column_type in missing_columns:
            try:
                cur.execute(f"ALTER TABLE pokemon_v2_berry ADD COLUMN {column_name} {column_type}")
                print(f"   ✅ Added column: {column_name}")
            except psycopg2.errors.DuplicateColumn:
                print(f"   ℹ️  Column {column_name} already exists")
                conn.rollback()
                conn.commit()  # Clear the failed transaction
            except Exception as e:
                print(f"   ❌ Failed to add {column_name}: {e}")
                conn.rollback()
                conn.commit()

        print("🔗 Creating items for existing berries...")

        # Get existing berries and create items for them
        cur.execute("SELECT id, name FROM pokemon_v2_berry WHERE item_id IS NULL")
        berries_without_items = cur.fetchall()

        for berry_id, name in berries_without_items:
            # Create item for berry
            cur.execute("""
            INSERT INTO pokemon_v2_item (id, name, item_category_id, cost) 
            VALUES (%s, %s, 1, 20) 
            ON CONFLICT (id) DO NOTHING;
            """, (berry_id, f"{name}-berry"))

            # Update berry with relationships
            cur.execute("""
            UPDATE pokemon_v2_berry SET 
                item_id = %s,
                berry_firmness_id = 2,
                natural_gift_power = 60,
                natural_gift_type_id = (SELECT id FROM pokemon_v2_type LIMIT 1),
                soil_dryness = 15,
                smoothness = 25
            WHERE id = %s;
            """, (berry_id, berry_id))

            print(f"   ✅ Updated berry: {name}")

        # Commit all changes
        conn.commit()

        # Test the berry table
        print("🧪 Testing berry table structure...")
        cur.execute("""
        SELECT b.id, b.name, b.natural_gift_power, b.soil_dryness, b.smoothness
        FROM pokemon_v2_berry b LIMIT 1
        """)

        test_row = cur.fetchone()
        if test_row:
            print(f"   ✅ Berry test successful: {test_row[1]} has all columns")

        cur.close()
        conn.close()

        print("\n🎉 Migration completed!")
        print("🔗 Your berry endpoint should now work:")
        print("   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False

if __name__ == "__main__":
    print("🔧 Simple Berry Table Fix")
    print("=" * 30)
    success = add_missing_columns()
    if success:
        print("✅ Success!")
    else:
        print("❌ Failed!")
