#!/usr/bin/env python3
"""
Manual fix for missing contest_type_id column in pokemon_v2_berryflavor table
"""
import os
import psycopg2

RAILWAY_DB_URL = os.environ.get('DATABASE_URL') or input("Enter your Railway DATABASE_URL: ").strip()

def fix_berryflavor_table():
    """Add missing contest_type_id column to pokemon_v2_berryflavor table"""
    try:
        conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = conn.cursor()

        print("🔧 Fixing pokemon_v2_berryflavor table...")

        # Check current structure
        cur.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'pokemon_v2_berryflavor' 
        ORDER BY ordinal_position
        """)
        existing_cols = [row[0] for row in cur.fetchall()]
        print(f"Current columns: {existing_cols}")

        # Add missing contest_type_id column if it doesn't exist
        if 'contest_type_id' not in existing_cols:
            print("Adding missing contest_type_id column...")

            # First create contest_type table if it doesn't exist
            cur.execute("""
            CREATE TABLE IF NOT EXISTS pokemon_v2_contesttype (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE
            )
            """)

            # Add contest types
            contest_types = [
                (1, 'cool'), (2, 'beauty'), (3, 'cute'), (4, 'smart'), (5, 'tough')
            ]

            for type_id, name in contest_types:
                cur.execute("""
                INSERT INTO pokemon_v2_contesttype (id, name) 
                VALUES (%s, %s) 
                ON CONFLICT (id) DO NOTHING
                """, (type_id, name))

            # Add the missing column
            cur.execute("""
            ALTER TABLE pokemon_v2_berryflavor 
            ADD COLUMN contest_type_id INTEGER REFERENCES pokemon_v2_contesttype(id)
            """)

            # Set default values for existing berries
            cur.execute("""
            UPDATE pokemon_v2_berryflavor 
            SET contest_type_id = 1 
            WHERE contest_type_id IS NULL
            """)

            print("✅ Added contest_type_id column with default values")
        else:
            print("ℹ️ contest_type_id column already exists")

        conn.commit()

        # Test the fix
        cur.execute("""
        SELECT bf.id, bf.name, bf.contest_type_id, ct.name as contest_name
        FROM pokemon_v2_berryflavor bf
        LEFT JOIN pokemon_v2_contesttype ct ON bf.contest_type_id = ct.id
        LIMIT 3
        """)

        results = cur.fetchall()
        print("\n🧪 Test query results:")
        for row in results:
            print(f"   Berry Flavor {row[0]}: {row[1]} -> Contest Type: {row[3]}")

        cur.close()
        conn.close()

        print("\n✅ Berry flavor table fixed!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_berry_endpoints():
    """Test if berry endpoints work now"""
    print("\n🧪 Testing berry endpoints...")

    import urllib.request
    import json

    endpoints = [
        ('Berry List', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/'),
        ('Berry Detail', 'https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/')
    ]

    for name, url in endpoints:
        try:
            print(f"   Testing {name}...")
            response = urllib.request.urlopen(url, timeout=15)

            if response.getcode() == 200:
                data = json.loads(response.read())
                if 'results' in data:
                    print(f"   ✅ {name}: Working ({data['count']} items)")
                elif 'name' in data:
                    print(f"   ✅ {name}: Working (detail for {data['name']})")
                else:
                    print(f"   ✅ {name}: Working (got valid JSON)")
                return True
            else:
                print(f"   ❌ {name}: HTTP {response.getcode()}")
                return False

        except Exception as e:
            print(f"   ❌ {name}: {str(e)[:100]}...")
            return False

    return True

if __name__ == "__main__":
    print("🔧 Manual Berry Flavor Table Fix")
    print("=" * 40)

    if fix_berryflavor_table():
        print("\n🚀 Testing endpoints after fix...")
        if test_berry_endpoints():
            print("\n🎉 SUCCESS! Berry endpoints are now working!")
        else:
            print("\n⚠️ Table fixed but endpoints still have issues")
    else:
        print("\n❌ Failed to fix table")
