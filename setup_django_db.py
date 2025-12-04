#!/usr/bin/env python3
"""
Railway Database Setup - Using Django Models
This version uses the actual Django models to ensure compatibility
"""
import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Force Railway environment detection
os.environ['RAILWAY_ENVIRONMENT'] = 'production'

def setup_django():
    """Initialize Django"""
    django.setup()

def run_migrations():
    """Run Django migrations"""
    from django.core.management import execute_from_command_line
    print("🔄 Running Django migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Migrations completed!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def load_sample_data():
    """Load sample data using Django models"""
    from pokemon_v2.models import Pokemon, Ability, Type, Berry, PokemonSpecies

    print("🎓 Loading sample data...")

    try:
        # Create species first (required for Pokemon)
        species_data = [
            {"id": 1, "name": "bulbasaur"},
            {"id": 4, "name": "charmander"},
            {"id": 7, "name": "squirtle"},
            {"id": 25, "name": "pikachu"},
            {"id": 150, "name": "mewtwo"},
        ]

        print("📝 Creating Pokemon species...")
        for species_info in species_data:
            species, created = PokemonSpecies.objects.get_or_create(
                id=species_info["id"],
                defaults={"name": species_info["name"]}
            )
            status = "✅ Created" if created else "ℹ️  Exists"
            print(f"   {status}: {species.name}")

        # Create types
        types_data = [
            {"id": 1, "name": "grass"},
            {"id": 2, "name": "poison"},
            {"id": 3, "name": "fire"},
            {"id": 4, "name": "water"},
            {"id": 5, "name": "electric"},
            {"id": 6, "name": "psychic"},
        ]

        print("🏷️  Creating types...")
        for type_info in types_data:
            type_obj, created = Type.objects.get_or_create(
                id=type_info["id"],
                defaults={"name": type_info["name"]}
            )
            status = "✅ Created" if created else "ℹ️  Exists"
            print(f"   {status}: {type_obj.name}")

        # Create abilities
        abilities_data = [
            {"id": 1, "name": "overgrow"},
            {"id": 2, "name": "chlorophyll"},
            {"id": 3, "name": "blaze"},
            {"id": 4, "name": "solar-power"},
            {"id": 5, "name": "torrent"},
            {"id": 6, "name": "rain-dish"},
            {"id": 7, "name": "static"},
            {"id": 8, "name": "lightning-rod"},
        ]

        print("💪 Creating abilities...")
        for ability_info in abilities_data:
            ability, created = Ability.objects.get_or_create(
                id=ability_info["id"],
                defaults={"name": ability_info["name"]}
            )
            status = "✅ Created" if created else "ℹ️  Exists"
            print(f"   {status}: {ability.name}")

        # Create Pokemon
        pokemon_data = [
            {"id": 1, "name": "bulbasaur", "species_id": 1, "height": 7, "weight": 69, "base_experience": 64},
            {"id": 4, "name": "charmander", "species_id": 4, "height": 6, "weight": 85, "base_experience": 62},
            {"id": 7, "name": "squirtle", "species_id": 7, "height": 5, "weight": 90, "base_experience": 63},
            {"id": 25, "name": "pikachu", "species_id": 25, "height": 4, "weight": 60, "base_experience": 112},
            {"id": 150, "name": "mewtwo", "species_id": 150, "height": 20, "weight": 1220, "base_experience": 340},
        ]

        print("🐾 Creating Pokemon...")
        for poke_info in pokemon_data:
            species = PokemonSpecies.objects.get(id=poke_info["species_id"])
            pokemon, created = Pokemon.objects.get_or_create(
                id=poke_info["id"],
                defaults={
                    "name": poke_info["name"],
                    "pokemon_species": species,
                    "height": poke_info["height"],
                    "weight": poke_info["weight"],
                    "base_experience": poke_info["base_experience"],
                    "is_default": True,
                    "order": poke_info["id"],
                }
            )
            status = "✅ Created" if created else "ℹ️  Exists"
            print(f"   {status}: {pokemon.name}")

        # Create berries
        berries_data = [
            {"id": 1, "name": "cheri"},
            {"id": 2, "name": "chesto"},
            {"id": 3, "name": "pecha"},
            {"id": 4, "name": "rawst"},
            {"id": 5, "name": "aspear"},
        ]

        print("🫐 Creating berries...")
        for berry_info in berries_data:
            berry, created = Berry.objects.get_or_create(
                id=berry_info["id"],
                defaults={"name": berry_info["name"]}
            )
            status = "✅ Created" if created else "ℹ️  Exists"
            print(f"   {status}: {berry.name}")

        # Summary
        pokemon_count = Pokemon.objects.count()
        ability_count = Ability.objects.count()
        type_count = Type.objects.count()
        berry_count = Berry.objects.count()

        print(f"\n🎉 Sample data loaded successfully!")
        print(f"📊 Database summary:")
        print(f"   Pokemon: {pokemon_count}")
        print(f"   Abilities: {ability_count}")
        print(f"   Types: {type_count}")
        print(f"   Berries: {berry_count}")

        return True

    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        print("💡 This might be due to model relationships or missing migrations")
        return False

def main():
    print("🚂 Railway Database Setup - Django Method")
    print("=" * 50)

    # Setup Django
    try:
        setup_django()
        print("✅ Django initialized")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return

    # Run migrations
    if not run_migrations():
        print("❌ Stopping due to migration failure")
        return

    # Load sample data
    if load_sample_data():
        print(f"\n🎓 Educational Pokemon API ready!")
        print(f"🔗 Test your endpoints:")
        print(f"   /api/v2/writable-pokemon/")
        print(f"   /api/v2/writable-ability/")
        print(f"   /api/v2/writable-type/")
        print(f"   /api/v2/writable-berry/")
    else:
        print("❌ Sample data loading failed")

if __name__ == "__main__":
    main()
