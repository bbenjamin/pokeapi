#!/usr/bin/env python3
"""
Direct SQLite to PostgreSQL Migration
Export SQLite data and import directly to Railway PostgreSQL
"""

import sqlite3
import psycopg2
import json

RAILWAY_DB_URL = os.environ.get('DATABASE_URL') or input("Enter your Railway DATABASE_URL: ").strip()

def export_sqlite_tables():
    """Export data from SQLite database"""
    print("📤 Exporting data from SQLite database...")

    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_conn.row_factory = sqlite3.Row  # Enable column access by name
        cur = sqlite_conn.cursor()

        # Get all pokemon_v2 tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'pokemon_v2_%'")
        tables = [row[0] for row in cur.fetchall()]

        print(f"   📊 Found {len(tables)} tables to export")

        exported_data = {}

        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]

            if count > 0:
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                exported_data[table] = [dict(row) for row in rows]
                print(f"   ✅ {table}: {count} records")
            else:
                print(f"   ⚠️ {table}: empty")

        sqlite_conn.close()

        if exported_data:
            print(f"   📁 Total tables with data: {len(exported_data)}")
            return exported_data
        else:
            print("   ❌ No data found in SQLite database")
            return None

    except Exception as e:
        print(f"   ❌ SQLite export error: {e}")
        return None

def import_to_railway(exported_data):
    """Import data to Railway PostgreSQL"""
    print("📥 Importing data to Railway PostgreSQL...")

    try:
        # Connect to Railway PostgreSQL
        pg_conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = pg_conn.cursor()

        # First, create any missing tables by checking what we have
        for table_name, rows in exported_data.items():
            if not rows:
                continue

            try:
                # Test if table exists and has the right columns
                cur.execute(f"SELECT COUNT(*) FROM {table_name} LIMIT 1")
                print(f"   ℹ️ Table {table_name} exists")
            except:
                print(f"   ⚠️ Table {table_name} missing - would need creation")
                continue

            # Clear existing data
            cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")

            # Import data
            if rows:
                # Get column names from first row
                columns = list(rows[0].keys())

                # Build INSERT statement
                placeholders = ', '.join(['%s'] * len(columns))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

                # Insert all rows
                for row in rows:
                    values = [row[col] for col in columns]
                    cur.execute(insert_sql, values)

                print(f"   ✅ {table_name}: {len(rows)} records imported")

        # Commit all changes
        pg_conn.commit()
        cur.close()
        pg_conn.close()

        print("   💾 All data committed to Railway!")
        return True

    except Exception as e:
        print(f"   ❌ Railway import error: {e}")
        if 'pg_conn' in locals():
            pg_conn.rollback()
        return False

def verify_migration():
    """Verify the migration was successful"""
    print("🔍 Verifying migration...")

    try:
        pg_conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = pg_conn.cursor()

        # Check key tables
        key_tables = ['pokemon_v2_berry', 'pokemon_v2_pokemon', 'pokemon_v2_ability', 'pokemon_v2_type']

        all_good = True

        for table in key_tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"   ✅ {table}: {count} records")

                if count == 0:
                    all_good = False

            except Exception as e:
                print(f"   ❌ {table}: Error - {e}")
                all_good = False

        cur.close()
        pg_conn.close()

        return all_good

    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False

def main():
    print("🗃️ Direct SQLite → Railway PostgreSQL Migration")
    print("=" * 60)
    print("Direct data transfer from SQLite to Railway PostgreSQL\n")

    # Step 1: Export from SQLite
    exported_data = export_sqlite_tables()
    if not exported_data:
        print("\n❌ No data to export from SQLite.")
        return False

    # Step 2: Import to Railway
    print(f"\n🚂 Importing to Railway...")
    if not import_to_railway(exported_data):
        print("\n❌ Import to Railway failed.")
        return False

    # Step 3: Verify
    print(f"\n🔍 Verifying migration...")
    if verify_migration():
        print("\n🎉 Direct migration successful!")
        print("🔗 Test your endpoints:")
        print("   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")
        print("   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/")
        return True
    else:
        print("\n⚠️ Migration completed but verification failed.")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'✅ Success!' if success else '❌ Failed!'}")
    exit(0 if success else 1)
