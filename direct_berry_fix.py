#!/usr/bin/env python3
"""
Direct Berry Column Fix - No input required
"""
import psycopg2

DATABASE_URL = "postgresql://postgres:kmoVkYPUByqWiiBKNXAHCBCOuzMkQnGx@maglev.proxy.rlwy.net:39520/railway"

try:
    print("🔧 Fixing berry table columns...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Check existing columns
    cur.execute("""
    SELECT column_name FROM information_schema.columns 
    WHERE table_name = 'pokemon_v2_berry' 
    ORDER BY ordinal_position
    """)
    existing_cols = [row[0] for row in cur.fetchall()]
    print(f"Current columns: {existing_cols}")

    # Create support tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_v2_berryfirmness (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    )
    """)

    # Add firmness data
    firmness_values = [
        "INSERT INTO pokemon_v2_berryfirmness (id, name) VALUES (1, 'very-soft') ON CONFLICT DO NOTHING",
        "INSERT INTO pokemon_v2_berryfirmness (id, name) VALUES (2, 'soft') ON CONFLICT DO NOTHING",
        "INSERT INTO pokemon_v2_berryfirmness (id, name) VALUES (3, 'hard') ON CONFLICT DO NOTHING"
    ]

    for sql in firmness_values:
        try:
            cur.execute(sql)
        except:
            pass

    # Add missing columns
    missing_columns = [
        "ALTER TABLE pokemon_v2_berry ADD COLUMN IF NOT EXISTS natural_gift_power INTEGER DEFAULT 60",
        "ALTER TABLE pokemon_v2_berry ADD COLUMN IF NOT EXISTS soil_dryness INTEGER DEFAULT 15",
        "ALTER TABLE pokemon_v2_berry ADD COLUMN IF NOT EXISTS smoothness INTEGER DEFAULT 25",
        "ALTER TABLE pokemon_v2_berry ADD COLUMN IF NOT EXISTS berry_firmness_id INTEGER DEFAULT 2"
    ]

    for sql in missing_columns:
        try:
            cur.execute(sql)
            print(f"✅ Executed: {sql.split()[5]}")
        except Exception as e:
            print(f"⚠️ Skipped: {e}")

    conn.commit()

    # Test query
    cur.execute("SELECT id, name, natural_gift_power, soil_dryness FROM pokemon_v2_berry LIMIT 1")
    result = cur.fetchone()
    print(f"✅ Test successful: {result}")

    cur.close()
    conn.close()

    print("🎉 Berry table fixed!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
