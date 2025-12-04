#!/usr/bin/env python3
"""
Railway Database Configuration Checker
"""
import os
import sys

print("🔍 Railway Database Configuration Checker")
print("=" * 50)

# Check environment variables
print("\n🌍 Environment Variables:")
database_url = os.environ.get('DATABASE_URL')
railway_env = os.environ.get('RAILWAY_ENVIRONMENT')

if database_url:
    print(f"✅ DATABASE_URL found")
    # Mask the password for security
    masked_url = database_url
    if '@' in masked_url and ':' in masked_url:
        parts = masked_url.split('@')
        if len(parts) == 2:
            user_pass = parts[0].split('://', 1)[1]
            if ':' in user_pass:
                user, _ = user_pass.split(':', 1)
                host_part = parts[1]
                masked_url = f"postgresql://{user}:***@{host_part}"
    print(f"   URL: {masked_url}")
else:
    print("❌ DATABASE_URL not found")

if railway_env:
    print(f"✅ RAILWAY_ENVIRONMENT: {railway_env}")
else:
    print("⚠️  RAILWAY_ENVIRONMENT not set")

# Check if we can parse the database URL
if database_url:
    try:
        import dj_database_url
        parsed = dj_database_url.parse(database_url)
        print(f"\n📊 Parsed Database Configuration:")
        print(f"   Engine: {parsed.get('ENGINE', 'N/A')}")
        print(f"   Host: {parsed.get('HOST', 'N/A')}")
        print(f"   Port: {parsed.get('PORT', 'N/A')}")
        print(f"   Database: {parsed.get('NAME', 'N/A')}")
        print(f"   User: {parsed.get('USER', 'N/A')}")
    except ImportError:
        print("❌ dj-database-url not available")
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")

# Test Django configuration
print(f"\n⚙️  Django Configuration Test:")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()

    from django.conf import settings
    db_config = settings.DATABASES['default']

    print(f"   Engine: {db_config.get('ENGINE', 'N/A')}")
    print(f"   Host: {db_config.get('HOST', 'N/A')}")
    print(f"   Port: {db_config.get('PORT', 'N/A')}")
    print(f"   Database: {db_config.get('NAME', 'N/A')}")
    print(f"   User: {db_config.get('USER', 'N/A')}")

    # Test connection
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

except Exception as e:
    print(f"❌ Django setup failed: {e}")

print(f"\n🎯 Recommendations:")
if not database_url:
    print("1. Add PostgreSQL database service in Railway dashboard")
    print("2. Railway should automatically set DATABASE_URL")

if database_url and 'localhost' in database_url:
    print("1. DATABASE_URL points to localhost - this won't work on Railway")
    print("2. Make sure you're using Railway's PostgreSQL service")

print("3. Check Railway logs for detailed error messages")
print("4. Verify environment variables in Railway dashboard")
