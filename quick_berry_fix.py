import psycopg2

# Direct connection to fix the immediate issue
DATABASE_URL = "postgresql://postgres:kmoVkYPUByqWiiBKNXAHCBCOuzMkQnGx@maglev.proxy.rlwy.net:39520/railway"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    print("✅ Connected to Railway PostgreSQL")

    # Check current berry table structure
    cur.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'pokemon_v2_berry' 
    ORDER BY ordinal_position;
    """)

    existing_columns = [row[0] for row in cur.fetchall()]
    print(f"📊 Current berry table columns: {existing_columns}")

    # Add natural_gift_power if missing
    if 'natural_gift_power' not in existing_columns:
        cur.execute("ALTER TABLE pokemon_v2_berry ADD COLUMN natural_gift_power INTEGER DEFAULT 60")
        print("✅ Added natural_gift_power column")

    # Add soil_dryness if missing
    if 'soil_dryness' not in existing_columns:
        cur.execute("ALTER TABLE pokemon_v2_berry ADD COLUMN soil_dryness INTEGER DEFAULT 15")
        print("✅ Added soil_dryness column")

    # Add smoothness if missing
    if 'smoothness' not in existing_columns:
        cur.execute("ALTER TABLE pokemon_v2_berry ADD COLUMN smoothness INTEGER DEFAULT 25")
        print("✅ Added smoothness column")

    conn.commit()

    # Test query
    cur.execute("SELECT id, name, natural_gift_power FROM pokemon_v2_berry LIMIT 1")
    test_result = cur.fetchone()
    print(f"🧪 Test query successful: {test_result}")

    cur.close()
    conn.close()

    print("🎉 Berry table fixed!")
    print("🔗 Test: https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
