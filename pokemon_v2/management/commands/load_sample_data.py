from django.core.management.base import BaseCommand
from pokemon_v2.models import Pokemon, Ability, Type, Berry, PokemonSpecies

class Command(BaseCommand):
    help = 'Load sample Pokemon data for educational purposes'

    def handle(self, *args, **options):
        self.stdout.write("🎓 Loading educational Pokemon data...")

        try:
            # Create species first (required for Pokemon)
            species_data = [
                {"id": 1, "name": "bulbasaur"},
                {"id": 4, "name": "charmander"},
                {"id": 7, "name": "squirtle"},
                {"id": 25, "name": "pikachu"},
                {"id": 150, "name": "mewtwo"},
            ]

            self.stdout.write("📝 Creating Pokemon species...")
            for species_info in species_data:
                species, created = PokemonSpecies.objects.get_or_create(
                    id=species_info["id"],
                    defaults={"name": species_info["name"]}
                )
                status = "Created" if created else "Exists"
                self.stdout.write(f"   ✅ {status}: {species.name}")

            # Create types
            types_data = [
                {"id": 1, "name": "grass"},
                {"id": 2, "name": "poison"},
                {"id": 3, "name": "fire"},
                {"id": 4, "name": "water"},
                {"id": 5, "name": "electric"},
                {"id": 6, "name": "psychic"},
            ]

            self.stdout.write("🏷️  Creating types...")
            for type_info in types_data:
                type_obj, created = Type.objects.get_or_create(
                    id=type_info["id"],
                    defaults={"name": type_info["name"]}
                )
                status = "Created" if created else "Exists"
                self.stdout.write(f"   ✅ {status}: {type_obj.name}")

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

            self.stdout.write("💪 Creating abilities...")
            for ability_info in abilities_data:
                ability, created = Ability.objects.get_or_create(
                    id=ability_info["id"],
                    defaults={"name": ability_info["name"]}
                )
                status = "Created" if created else "Exists"
                self.stdout.write(f"   ✅ {status}: {ability.name}")

            # Create Pokemon
            pokemon_data = [
                {"id": 1, "name": "bulbasaur", "species_id": 1, "height": 7, "weight": 69, "base_experience": 64},
                {"id": 4, "name": "charmander", "species_id": 4, "height": 6, "weight": 85, "base_experience": 62},
                {"id": 7, "name": "squirtle", "species_id": 7, "height": 5, "weight": 90, "base_experience": 63},
                {"id": 25, "name": "pikachu", "species_id": 25, "height": 4, "weight": 60, "base_experience": 112},
                {"id": 150, "name": "mewtwo", "species_id": 150, "height": 20, "weight": 1220, "base_experience": 340},
            ]

            self.stdout.write("🐾 Creating Pokemon...")
            for poke_info in pokemon_data:
                try:
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
                    status = "Created" if created else "Exists"
                    self.stdout.write(f"   ✅ {status}: {pokemon.name}")
                except Exception as e:
                    self.stdout.write(f"   ❌ Failed to create {poke_info['name']}: {e}")

            # Create berries
            berries_data = [
                {"id": 1, "name": "cheri"},
                {"id": 2, "name": "chesto"},
                {"id": 3, "name": "pecha"},
                {"id": 4, "name": "rawst"},
                {"id": 5, "name": "aspear"},
            ]

            self.stdout.write("🫐 Creating berries...")
            for berry_info in berries_data:
                berry, created = Berry.objects.get_or_create(
                    id=berry_info["id"],
                    defaults={"name": berry_info["name"]}
                )
                status = "Created" if created else "Exists"
                self.stdout.write(f"   ✅ {status}: {berry.name}")

            # Summary
            pokemon_count = Pokemon.objects.count()
            ability_count = Ability.objects.count()
            type_count = Type.objects.count()
            berry_count = Berry.objects.count()

            self.stdout.write(f"\n🎉 Sample data loaded successfully!")
            self.stdout.write(f"📊 Database summary:")
            self.stdout.write(f"   Pokemon: {pokemon_count}")
            self.stdout.write(f"   Abilities: {ability_count}")
            self.stdout.write(f"   Types: {type_count}")
            self.stdout.write(f"   Berries: {berry_count}")

        except Exception as e:
            self.stdout.write(f"❌ Error loading sample data: {e}")
            raise e
