import os
import psycopg2

conn = psycopg2.connect(os.environ.get('DATABASE_URL') or input("Enter your Railway DATABASE_URL: ").strip())
cur = conn.cursor()

# Create BerryFlavor table
cur.execute("CREATE TABLE IF NOT EXISTS pokemon_v2_berryflavor (id SERIAL PRIMARY KEY, name VARCHAR(100) UNIQUE)")

# Add flavors
cur.execute("INSERT INTO pokemon_v2_berryflavor (id, name) VALUES (1, 'spicy') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO pokemon_v2_berryflavor (id, name) VALUES (2, 'dry') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO pokemon_v2_berryflavor (id, name) VALUES (3, 'sweet') ON CONFLICT DO NOTHING")

# Create BerryFlavorMap table
cur.execute("CREATE TABLE IF NOT EXISTS pokemon_v2_berryflavormap (id SERIAL PRIMARY KEY, berry_id INTEGER, berry_flavor_id INTEGER, potency INTEGER DEFAULT 10)")

# Add sample mappings for berries 1-5
for berry_id in range(1, 6):
    cur.execute(f"INSERT INTO pokemon_v2_berryflavormap (berry_id, berry_flavor_id, potency) VALUES ({berry_id}, 1, 10)")
    cur.execute(f"INSERT INTO pokemon_v2_berryflavormap (berry_id, berry_flavor_id, potency) VALUES ({berry_id}, 3, 15)")

conn.commit()
cur.close()
conn.close()
print("Done!")
