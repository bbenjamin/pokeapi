#!/usr/bin/env python3
"""
Export Local Database and Import to Railway PostgreSQL
This script will dump your working local database and import it to Railway
"""

import subprocess
import psycopg2
import os
import sys

# Railway connection details
RAILWAY_DATABASE_URL = os.environ.get('DATABASE_URL') or input("Enter your Railway DATABASE_URL: ").strip()

def export_local_database():
    """Export local database to SQL dump file"""
    print("🔍 Looking for local database...")

    # Check if there's a local PostgreSQL database
    local_db_options = [
        "postgresql://localhost:5432/pokeapi",
        "postgresql://localhost:5432/pokemon",
        "postgresql://localhost:5432/django_pokeapi",
    ]

    # Also check for SQLite database (common for Django development)
    sqlite_files = [
        "db.sqlite3",
        "../db.sqlite3",
        "pokeapi.db",
        "pokemon.db"
    ]

    print("📋 Checking for local databases:")

    # Check SQLite files first
    for sqlite_file in sqlite_files:
        if os.path.exists(sqlite_file):
            print(f"   ✅ Found SQLite database: {sqlite_file}")
            return export_sqlite_database(sqlite_file)

    # Check PostgreSQL databases
    for db_url in local_db_options:
        try:
            conn = psycopg2.connect(db_url, connect_timeout=5)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM pokemon_v2_berry")
            berry_count = cur.fetchone()[0]
            cur.close()
            conn.close()

            if berry_count > 0:
                print(f"   ✅ Found working PostgreSQL database: {db_url}")
                return export_postgresql_database(db_url)

        except Exception as e:
            print(f"   ❌ Could not connect to {db_url}: {e}")

    print("\n❌ No working local database found!")
    print("💡 Options:")
    print("   1. Run 'python manage.py migrate' locally first")
    print("   2. Make sure your local database has data")
    print("   3. Provide your local DATABASE_URL manually")

    return None

def export_sqlite_database(sqlite_file):
    """Export SQLite database to PostgreSQL-compatible SQL"""
    print(f"📤 Exporting SQLite database: {sqlite_file}")

    try:
        # Use sqlite3 command to export
        dump_file = "local_db_dump.sql"

        cmd = f"sqlite3 {sqlite_file} .dump > {dump_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"   ✅ SQLite dump created: {dump_file}")
            return convert_sqlite_to_postgresql(dump_file)
        else:
            print(f"   ❌ SQLite dump failed: {result.stderr}")
            return None

    except Exception as e:
        print(f"   ❌ SQLite export error: {e}")
        return None

def export_postgresql_database(db_url):
    """Export PostgreSQL database using pg_dump"""
    print(f"📤 Exporting PostgreSQL database...")

    try:
        dump_file = "local_postgres_dump.sql"

        # Use pg_dump to create the dump
        cmd = f"pg_dump '{db_url}' > {dump_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"   ✅ PostgreSQL dump created: {dump_file}")
            return dump_file
        else:
            print(f"   ❌ pg_dump failed: {result.stderr}")
            return None

    except Exception as e:
        print(f"   ❌ PostgreSQL export error: {e}")
        return None

def convert_sqlite_to_postgresql(sqlite_dump):
    """Convert SQLite dump to PostgreSQL-compatible format"""
    print("🔄 Converting SQLite dump to PostgreSQL format...")

    try:
        with open(sqlite_dump, 'r') as f:
            content = f.read()

        # Basic SQLite to PostgreSQL conversions
        conversions = [
            ('AUTOINCREMENT', 'SERIAL'),
            ('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY'),
            ('datetime(', 'TIMESTAMP '),
            ("'t'", 'true'),
            ("'f'", 'false'),
        ]

        for old, new in conversions:
            content = content.replace(old, new)

        # Remove SQLite-specific commands
        lines = content.split('\n')
        filtered_lines = []

        for line in lines:
            if not any(skip in line for skip in [
                'PRAGMA', 'BEGIN TRANSACTION', 'COMMIT;', 'sqlite_sequence',
                'CREATE UNIQUE INDEX', 'sqlite_autoindex'
            ]):
                filtered_lines.append(line)

        postgres_dump = "postgres_compatible_dump.sql"
        with open(postgres_dump, 'w') as f:
            f.write('\n'.join(filtered_lines))

        print(f"   ✅ PostgreSQL-compatible dump created: {postgres_dump}")
        return postgres_dump

    except Exception as e:
        print(f"   ❌ Conversion error: {e}")
        return None

def clear_railway_database():
    """Clear existing Railway database tables"""
    print("🗑️ Clearing existing Railway database...")

    try:
        conn = psycopg2.connect(RAILWAY_DATABASE_URL)
        cur = conn.cursor()

        # Get all table names
        cur.execute("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public' AND tablename LIKE 'pokemon_v2_%'
        """)

        tables = [row[0] for row in cur.fetchall()]

        if tables:
            # Drop tables in reverse dependency order
            for table in reversed(tables):
                try:
                    cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    print(f"   ✅ Dropped table: {table}")
                except Exception as e:
                    print(f"   ⚠️ Could not drop {table}: {e}")

        # Also drop Django migration tables to start fresh
        cur.execute("DROP TABLE IF EXISTS django_migrations CASCADE")

        conn.commit()
        cur.close()
        conn.close()

        print("   ✅ Railway database cleared!")
        return True

    except Exception as e:
        print(f"   ❌ Error clearing database: {e}")
        return False

def import_to_railway(dump_file):
    """Import SQL dump to Railway PostgreSQL"""
    print(f"📥 Importing {dump_file} to Railway PostgreSQL...")

    try:
        # Use psql to import the dump
        cmd = f"psql '{RAILWAY_DATABASE_URL}' < {dump_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("   ✅ Import successful!")
            return True
        else:
            print(f"   ❌ Import failed: {result.stderr}")

            # Try alternative method - execute SQL directly
            print("   🔄 Trying direct SQL execution...")
            return import_sql_directly(dump_file)

    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def import_sql_directly(dump_file):
    """Import SQL by executing it directly with psycopg2"""
    print("📥 Executing SQL directly...")

    try:
        conn = psycopg2.connect(RAILWAY_DATABASE_URL)
        cur = conn.cursor()

        with open(dump_file, 'r') as f:
            sql_content = f.read()

        # Split into individual statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

        successful = 0
        failed = 0

        for i, stmt in enumerate(statements):
            try:
                cur.execute(stmt)
                successful += 1
                if i % 100 == 0:  # Progress indicator
                    print(f"   📊 Executed {i}/{len(statements)} statements...")
            except Exception as e:
                failed += 1
                if "already exists" not in str(e):
                    print(f"   ⚠️ Statement failed: {str(e)[:100]}...")

        conn.commit()
        cur.close()
        conn.close()

        print(f"   ✅ Direct execution completed!")
        print(f"   📊 Successful: {successful}, Failed: {failed}")

        return successful > failed

    except Exception as e:
        print(f"   ❌ Direct execution error: {e}")
        return False

def verify_import():
    """Verify that the import was successful"""
    print("🔍 Verifying import...")

    try:
        conn = psycopg2.connect(RAILWAY_DATABASE_URL)
        cur = conn.cursor()

        # Check key tables
        tables_to_check = [
            ('pokemon_v2_berry', 'berries'),
            ('pokemon_v2_pokemon', 'pokemon'),
            ('pokemon_v2_ability', 'abilities'),
            ('pokemon_v2_type', 'types'),
            ('pokemon_v2_berryflavormap', 'berry flavor mappings')
        ]

        all_good = True

        for table, description in tables_to_check:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"   ✅ {description}: {count} records")
            except Exception as e:
                print(f"   ❌ {description}: Table missing or error")
                all_good = False

        cur.close()
        conn.close()

        if all_good:
            print("\n🎉 Import verification successful!")
            print("🔗 Test your endpoints:")
            print("   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/")
            print("   https://pokeapi-production-2219.up.railway.app/api/v2/writable-berry/1/")

        return all_good

    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False

def main():
    print("🚂 Local Database → Railway Migration Tool")
    print("=" * 60)
    print("This will export your working local database and import it to Railway")
    print("to get a complete, working schema with all relationships.\n")

    # Step 1: Export local database
    dump_file = export_local_database()
    if not dump_file:
        print("\n❌ Could not export local database. Exiting.")
        return False

    # Step 2: Clear Railway database
    if not clear_railway_database():
        print("\n❌ Could not clear Railway database. Exiting.")
        return False

    # Step 3: Import to Railway
    if not import_to_railway(dump_file):
        print("\n❌ Import failed. Exiting.")
        return False

    # Step 4: Verify import
    if verify_import():
        print("\n🎉 Migration completed successfully!")
        print("🚂 Your Railway database now has the complete working schema!")

        # Clean up dump files
        try:
            os.remove(dump_file)
            print(f"🧹 Cleaned up dump file: {dump_file}")
        except:
            pass

        return True
    else:
        print("\n⚠️ Migration completed but verification failed.")
        print("💡 Try testing your endpoints manually.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
