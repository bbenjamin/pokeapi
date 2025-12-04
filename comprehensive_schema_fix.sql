-- Comprehensive fix for all missing Django model columns
-- Based on Pokemon v2 model structure

-- 1. Create MoveDamageClass table
CREATE TABLE IF NOT EXISTS pokemon_v2_movedamageclass (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

-- 2. Add move damage classes
INSERT INTO pokemon_v2_movedamageclass (id, name) VALUES
(1, 'status'),
(2, 'physical'),
(3, 'special')
ON CONFLICT (id) DO NOTHING;

-- 3. Add missing move_damage_class_id to Type table
ALTER TABLE pokemon_v2_type
ADD COLUMN IF NOT EXISTS move_damage_class_id INTEGER REFERENCES pokemon_v2_movedamageclass(id);

-- 4. Set default move damage class for existing types
UPDATE pokemon_v2_type
SET move_damage_class_id = 2  -- physical by default
WHERE move_damage_class_id IS NULL;

-- 5. Create Generation table if missing
CREATE TABLE IF NOT EXISTS pokemon_v2_generation (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    main_region_id INTEGER
);

-- 6. Add generations
INSERT INTO pokemon_v2_generation (id, name) VALUES
(1, 'generation-i'),
(2, 'generation-ii'),
(3, 'generation-iii'),
(4, 'generation-iv'),
(5, 'generation-v'),
(6, 'generation-vi'),
(7, 'generation-vii'),
(8, 'generation-viii'),
(9, 'generation-ix')
ON CONFLICT (id) DO NOTHING;

-- 7. Add missing generation_id to Type table
ALTER TABLE pokemon_v2_type
ADD COLUMN IF NOT EXISTS generation_id INTEGER REFERENCES pokemon_v2_generation(id);

-- 8. Set default generation for existing types
UPDATE pokemon_v2_type
SET generation_id = 1  -- generation-i by default
WHERE generation_id IS NULL;

-- 9. Fix Item table - ensure all required columns exist
ALTER TABLE pokemon_v2_item
ADD COLUMN IF NOT EXISTS cost INTEGER DEFAULT 0;

ALTER TABLE pokemon_v2_item
ADD COLUMN IF NOT EXISTS fling_power INTEGER;

-- 10. Create MoveDamageClass names table for completeness
CREATE TABLE IF NOT EXISTS pokemon_v2_movedamageclassname (
    id SERIAL PRIMARY KEY,
    move_damage_class_id INTEGER REFERENCES pokemon_v2_movedamageclass(id),
    language_id INTEGER DEFAULT 1,
    name VARCHAR(100)
);

-- 11. Create Language table if needed
CREATE TABLE IF NOT EXISTS pokemon_v2_language (
    id SERIAL PRIMARY KEY,
    iso639 VARCHAR(10),
    iso3166 VARCHAR(10),
    name VARCHAR(100) UNIQUE,
    official BOOLEAN DEFAULT true,
    order_value INTEGER
);

-- 12. Add basic language
INSERT INTO pokemon_v2_language (id, name, iso639, iso3166, official, order_value) VALUES
(1, 'en', 'en', 'US', true, 1)
ON CONFLICT (id) DO NOTHING;

-- 13. Verify all the fixes
SELECT 't.id' as table_check, 'Type table' as description,
       t.id, t.name, t.generation_id, t.move_damage_class_id,
       g.name as generation_name, mdc.name as damage_class_name
FROM pokemon_v2_type t
LEFT JOIN pokemon_v2_generation g ON t.generation_id = g.id
LEFT JOIN pokemon_v2_movedamageclass mdc ON t.move_damage_class_id = mdc.id
LIMIT 5;

SELECT 'i.id' as table_check, 'Item table' as description,
       i.id, i.name, i.cost, i.fling_power, i.item_fling_effect_id
FROM pokemon_v2_item i
LIMIT 5;

SELECT 'Complete schema check' as status;
