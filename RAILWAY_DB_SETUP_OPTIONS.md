# 🗄️ RAILWAY POSTGRESQL - MULTIPLE SETUP OPTIONS

## 🔍 **Current Situation**
Your Railway PostgreSQL database exists but has no tables or data. The automatic deployment didn't work as expected.

## 🛠️ **Option 1: Direct Python Script (Recommended)**

I've created a script that connects directly to your Railway PostgreSQL and sets up everything:

```bash
# Install psycopg2 for direct PostgreSQL connection
pip install psycopg2-binary

# Run the direct setup script
python setup_railway_db.py
```

**What it does:**
- ✅ Connects directly to Railway PostgreSQL
- ✅ Creates all necessary tables
- ✅ Populates with sample Pokemon, abilities, types, berries
- ✅ Verifies data was loaded correctly

## 🌐 **Option 2: Railway Web Console**

1. **Go to Railway Dashboard**
2. **Click your PostgreSQL service** (not Django service)
3. **Click "Query" or "Console" tab**
4. **Run SQL directly:**

```sql
-- Create and populate types table
CREATE TABLE IF NOT EXISTS pokemon_v2_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO pokemon_v2_type (id, name) VALUES 
(1, 'grass'), (2, 'poison'), (3, 'fire'), 
(4, 'water'), (5, 'electric'), (6, 'psychic')
ON CONFLICT (id) DO NOTHING;

-- Create and populate abilities table
CREATE TABLE IF NOT EXISTS pokemon_v2_ability (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO pokemon_v2_ability (id, name) VALUES 
(1, 'overgrow'), (2, 'chlorophyll'), (3, 'blaze'), (4, 'solar-power'),
(5, 'torrent'), (6, 'rain-dish'), (7, 'static'), (8, 'lightning-rod')
ON CONFLICT (id) DO NOTHING;

-- Create and populate pokemon table
CREATE TABLE IF NOT EXISTS pokemon_v2_pokemon (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    height INTEGER,
    weight INTEGER,
    base_experience INTEGER
);

INSERT INTO pokemon_v2_pokemon (id, name, height, weight, base_experience) VALUES 
(1, 'bulbasaur', 7, 69, 64),
(4, 'charmander', 6, 85, 62),
(7, 'squirtle', 5, 90, 63),
(25, 'pikachu', 4, 60, 112),
(150, 'mewtwo', 20, 1220, 340)
ON CONFLICT (id) DO NOTHING;

-- Create and populate berry table
CREATE TABLE IF NOT EXISTS pokemon_v2_berry (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    growth_time INTEGER,
    max_harvest INTEGER,
    size INTEGER
);

INSERT INTO pokemon_v2_berry (id, name, growth_time, max_harvest, size) VALUES 
(1, 'cheri', 3, 5, 20),
(2, 'chesto', 3, 5, 80),
(3, 'pecha', 3, 5, 40),
(4, 'rawst', 3, 5, 32),
(5, 'aspear', 3, 5, 50)
ON CONFLICT (id) DO NOTHING;
```

## 💻 **Option 3: Local PostgreSQL Client**

If you have `psql` installed locally:

```bash
# Get your DATABASE_URL from Railway dashboard
# Then connect directly:
psql "your-railway-database-url-here"

# Run the SQL commands from Option 2
```

## 📊 **Option 4: Fix Automatic Deployment**

Check why automatic deployment didn't work:

1. **Check Railway Deployment Logs:**
   - Go to Railway → Your Django Service → "Deploy Logs"
   - Look for migration errors

2. **Check Procfile is Working:**
   ```bash
   # Your Procfile should have:
   release: python manage.py migrate && python manage.py load_sample_data
   ```

3. **Manual Trigger of Release Command:**
   - In Railway dashboard, go to Django service
   - Look for "Run Command" or "Console" option
   - Run: `python manage.py migrate && python manage.py load_sample_data`

## 🎯 **Recommended Approach**

**Try Option 1 first (Python script):**

```bash
# Install required dependency
pip install psycopg2-binary

# Run the setup script
python setup_railway_db.py
```

**Get your DATABASE_URL from:**
1. Railway Dashboard → PostgreSQL service → "Connect" tab
2. Copy the "DATABASE_URL" value
3. Paste when prompted by the script

## ✅ **Verification**

After any method, test your API:
- **Root:** `https://your-app.railway.app/`
- **Pokemon:** `https://your-app.railway.app/api/v2/writable-pokemon/`
- **Docs:** `https://your-app.railway.app/api/v2/schema/swagger-ui/`

You should see:
```json
{
    "count": 5,
    "results": [
        {"id": 1, "name": "bulbasaur", "height": 7, "weight": 69},
        {"id": 4, "name": "charmander", "height": 6, "weight": 85},
        ...
    ]
}
```

## 🚨 **If All Options Fail**

There might be a Django model mismatch. Let me know the exact error messages and I'll create a Django-compatible solution that matches your actual models.

**Start with Option 1 (Python script) - it's the most reliable!**
