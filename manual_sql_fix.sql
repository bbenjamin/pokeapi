-- Manual SQL commands to fix the missing contest_type_id column
-- Run these directly in Railway PostgreSQL console or psql

-- 1. Create contest_type table if missing
CREATE TABLE IF NOT EXISTS pokemon_v2_contesttype (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

-- 2. Add contest types
INSERT INTO pokemon_v2_contesttype (id, name) VALUES
(1, 'cool'),
(2, 'beauty'),
(3, 'cute'),
(4, 'smart'),
(5, 'tough')
ON CONFLICT (id) DO NOTHING;

-- 3. Add missing contest_type_id column to berry flavor table
ALTER TABLE pokemon_v2_berryflavor
ADD COLUMN IF NOT EXISTS contest_type_id INTEGER REFERENCES pokemon_v2_contesttype(id);

-- 4. Set default contest type for existing berry flavors
UPDATE pokemon_v2_berryflavor
SET contest_type_id = 1
WHERE contest_type_id IS NULL;

-- 5. Verify the fix
SELECT
    bf.id,
    bf.name as flavor_name,
    bf.contest_type_id,
    ct.name as contest_type_name
FROM pokemon_v2_berryflavor bf
LEFT JOIN pokemon_v2_contesttype ct ON bf.contest_type_id = ct.id;

-- Expected output should show all berry flavors with contest_type_id populated

-- 6. Create item_fling_effect table if missing
CREATE TABLE IF NOT EXISTS pokemon_v2_itemflingeffect (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

-- 7. Add basic item fling effects
INSERT INTO pokemon_v2_itemflingeffect (id, name) VALUES
(1, 'badly-poison'),
(2, 'burn'),
(3, 'berry-effect'),
(4, 'herb-effect'),
(5, 'paralyze'),
(6, 'poison'),
(7, 'flinch')
ON CONFLICT (id) DO NOTHING;

-- 8. Add missing item_fling_effect_id column to item table
ALTER TABLE pokemon_v2_item
ADD COLUMN IF NOT EXISTS item_fling_effect_id INTEGER REFERENCES pokemon_v2_itemflingeffect(id);

-- 9. Set default fling effect for existing items (can be NULL for most items)
UPDATE pokemon_v2_item
SET item_fling_effect_id = NULL
WHERE item_fling_effect_id IS NULL;

-- 10. Verify the item table fix
SELECT
    i.id,
    i.name as item_name,
    i.item_fling_effect_id,
    ife.name as fling_effect_name
FROM pokemon_v2_item i
LEFT JOIN pokemon_v2_itemflingeffect ife ON i.item_fling_effect_id = ife.id
LIMIT 5;

-- Expected output should show item_fling_effect_id populated where applicable
