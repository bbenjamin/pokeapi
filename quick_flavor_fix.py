#!/usr/bin/env python3
"""
Quick fix for missing pokemon_v2_berryflavormap table
"""
import psycopg2

DATABASE_URL = "postgresql://postgres:kmoVkYPUByqWiiBKNXAHCBCOuzMkQnGx@maglev.proxy.rlwy.net:39520/railway"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("Creating missing BerryFlavorMap table...")

    # Create BerryFlavor table first
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_v2_berryflavor (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    )
    """)

    # Add basic flavors
    flavors = ['spicy', 'dry', 'sweet', 'bitter', 'sour']
    for i, flavor in enumerate(flavors, 1):
        cur.execute(f"INSERT INTO pokemon_v2_berryflavor (id, name) VALUES ({i}, '{flavor}') ON CONFLICT DO NOTHING")

    # Create BerryFlavorMap table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_v2_berryflavormap (
        id SERIAL PRIMARY KEY,
        berry_id INTEGER REFERENCES pokemon_v2_berry(id),
        berry_flavor_id INTEGER REFERENCES pokemon_v2_berryflavor(id),
        potency INTEGER DEFAULT 10
    )
    """)

    # Add sample flavor mappings for existing berries
    cur.execute("SELECT id FROM pokemon_v2_berry")
    berry_ids = [row[0] for row in cur.fetchall()]

    for berry_id in berry_ids:
        # Add 2 flavors per berry
        cur.execute(f"""
        INSERT INTO pokemon_v2_berryflavormap (berry_id, berry_flavor_id, potency) 
        VALUES ({berry_id}, 1, 10), ({berry_id}, 3, 15)
        ON CONFLICT DO NOTHING
        """)

    conn.commit()

    # Test
    cur.execute("SELECT COUNT(*) FROM pokemon_v2_berryflavormap")
    count = cur.fetchone()[0]
    print(f"✅ Created BerryFlavorMap with {count} entries")

    cur.close()
    conn.close()

    print("🎉 Berry detail endpoint should work now!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
