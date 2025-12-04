import os
import psycopg2

conn = psycopg2.connect(os.environ.get('DATABASE_URL') or input("Enter your Railway DATABASE_URL: ").strip())
cur = conn.cursor()

print("Creating all missing berry-related tables...")

# Create Item tables (needed for Berry.item relationship)
cur.execute("""
CREATE TABLE IF NOT EXISTS pokemon_v2_itempocket (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pokemon_v2_itemcategory (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100) UNIQUE,
    item_pocket_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pokemon_v2_item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    item_category_id INTEGER,
    cost INTEGER DEFAULT 0
)
""")

# Add basic item data
cur.execute("INSERT INTO pokemon_v2_itempocket (id, name) VALUES (1, 'berries') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO pokemon_v2_itemcategory (id, name, item_pocket_id) VALUES (1, 'berry', 1) ON CONFLICT DO NOTHING")

# Create items for berries 1-5
for i in range(1, 6):
    cur.execute(f"INSERT INTO pokemon_v2_item (id, name, item_category_id, cost) VALUES ({i}, 'berry-{i}', 1, 20) ON CONFLICT DO NOTHING")

# Create BerryFirmness table
cur.execute("""
CREATE TABLE IF NOT EXISTS pokemon_v2_berryfirmness (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
)
""")

# Add firmness data
firmness_values = ['very-soft', 'soft', 'hard', 'very-hard', 'super-hard']
for i, firmness in enumerate(firmness_values, 1):
    cur.execute(f"INSERT INTO pokemon_v2_berryfirmness (id, name) VALUES ({i}, '{firmness}') ON CONFLICT DO NOTHING")

# Add item_id and berry_firmness_id to berries if missing
try:
    cur.execute("ALTER TABLE pokemon_v2_berry ADD COLUMN IF NOT EXISTS item_id INTEGER")
    cur.execute("ALTER TABLE pokemon_v2_berry ADD COLUMN IF NOT EXISTS berry_firmness_id INTEGER")
except:
    pass

# Update existing berries with relationships
for i in range(1, 6):
    cur.execute(f"""
    UPDATE pokemon_v2_berry 
    SET item_id = {i}, berry_firmness_id = 2
    WHERE id = {i} AND (item_id IS NULL OR berry_firmness_id IS NULL)
    """)

conn.commit()
cur.close()
conn.close()
print("✅ All berry-related tables created!")
print("🧪 Test: https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/")
