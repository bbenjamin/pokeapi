from django.core.management.base import BaseCommand
from pokemon_v2.models import (
    Pokemon, PokemonSpecies, Ability, Type, Berry, BerryFirmness,
    Item, ItemCategory, ItemPocket
)

class Command(BaseCommand):
    help = 'Load educational sample data that matches Django models properly'

    def handle(self, *args, **options):
        self.stdout.write("🎓 Loading educational Pokemon data with proper Django models...")

        try:
            # Create required related objects first

            # Create ItemPocket and ItemCategory for HasItem relationships
            item_pocket, _ = ItemPocket.objects.get_or_create(
                id=1,
                defaults={'name': 'berries'}
            )

            item_category, _ = ItemCategory.objects.get_or_create(
                id=1,
                defaults={'name': 'berry', 'item_pocket': item_pocket}
            )

            # Create Items for berries (required by HasItem)
            berry_items = [
                {'id': 1, 'name': 'cheri-berry'},
                {'id': 2, 'name': 'chesto-berry'},
                {'id': 3, 'name': 'pecha-berry'},
                {'id': 4, 'name': 'rawst-berry'},
                {'id': 5, 'name': 'aspear-berry'},
            ]

            for item_data in berry_items:
                item, created = Item.objects.get_or_create(
                    id=item_data['id'],
                    defaults={
                        'name': item_data['name'],
                        'item_category': item_category,
                        'cost': 20
                    }
                )
                if created:
                    self.stdout.write(f"   ✅ Created Item: {item.name}")

            # Create BerryFirmness
            firmness_data = [
                {'id': 1, 'name': 'very-soft'},
                {'id': 2, 'name': 'soft'},
                {'id': 3, 'name': 'hard'},
                {'id': 4, 'name': 'very-hard'},
                {'id': 5, 'name': 'super-hard'},
            ]

            for firmness_info in firmness_data:
                firmness, created = BerryFirmness.objects.get_or_create(
                    id=firmness_info['id'],
                    defaults={'name': firmness_info['name']}
                )
                if created:
                    self.stdout.write(f"   ✅ Created BerryFirmness: {firmness.name}")

            # Create Types
            types_data = [
                {'id': 1, 'name': 'normal'},
                {'id': 2, 'name': 'fighting'},
                {'id': 3, 'name': 'flying'},
                {'id': 4, 'name': 'poison'},
                {'id': 5, 'name': 'ground'},
                {'id': 6, 'name': 'rock'},
                {'id': 7, 'name': 'bug'},
                {'id': 8, 'name': 'ghost'},
                {'id': 9, 'name': 'steel'},
                {'id': 10, 'name': 'fire'},
                {'id': 11, 'name': 'water'},
                {'id': 12, 'name': 'grass'},
                {'id': 13, 'name': 'electric'},
                {'id': 14, 'name': 'psychic'},
                {'id': 15, 'name': 'ice'},
                {'id': 16, 'name': 'dragon'},
                {'id': 17, 'name': 'dark'},
                {'id': 18, 'name': 'fairy'},
            ]

            for type_info in types_data:
                type_obj, created = Type.objects.get_or_create(
                    id=type_info['id'],
                    defaults={'name': type_info['name']}
                )
                if created:
                    self.stdout.write(f"   ✅ Created Type: {type_obj.name}")

            # Create Abilities
            abilities_data = [
                {'id': 1, 'name': 'stench'},
                {'id': 2, 'name': 'drizzle'},
                {'id': 3, 'name': 'speed-boost'},
                {'id': 4, 'name': 'battle-armor'},
                {'id': 5, 'name': 'sturdy'},
                {'id': 6, 'name': 'damp'},
                {'id': 7, 'name': 'limber'},
                {'id': 8, 'name': 'sand-veil'},
                {'id': 9, 'name': 'static'},
                {'id': 10, 'name': 'volt-absorb'},
            ]

            for ability_info in abilities_data:
                ability, created = Ability.objects.get_or_create(
                    id=ability_info['id'],
                    defaults={
                        'name': ability_info['name'],
                        'is_main_series': True
                    }
                )
                if created:
                    self.stdout.write(f"   ✅ Created Ability: {ability.name}")

            # Create Pokemon Species (required for Pokemon)
            species_data = [
                {'id': 1, 'name': 'bulbasaur'},
                {'id': 4, 'name': 'charmander'},
                {'id': 7, 'name': 'squirtle'},
                {'id': 25, 'name': 'pikachu'},
                {'id': 150, 'name': 'mewtwo'},
            ]

            for species_info in species_data:
                species, created = PokemonSpecies.objects.get_or_create(
                    id=species_info['id'],
                    defaults={
                        'name': species_info['name'],
                        'order': species_info['id'],
                        'gender_rate': 1,
                        'capture_rate': 45,
                        'base_happiness': 70,
                        'is_baby': False,
                        'hatch_counter': 20
                    }
                )
                if created:
                    self.stdout.write(f"   ✅ Created PokemonSpecies: {species.name}")

            # Create Pokemon
            pokemon_data = [
                {'id': 1, 'name': 'bulbasaur', 'species_id': 1, 'height': 7, 'weight': 69, 'base_experience': 64},
                {'id': 4, 'name': 'charmander', 'species_id': 4, 'height': 6, 'weight': 85, 'base_experience': 62},
                {'id': 7, 'name': 'squirtle', 'species_id': 7, 'height': 5, 'weight': 90, 'base_experience': 63},
                {'id': 25, 'name': 'pikachu', 'species_id': 25, 'height': 4, 'weight': 60, 'base_experience': 112},
                {'id': 150, 'name': 'mewtwo', 'species_id': 150, 'height': 20, 'weight': 1220, 'base_experience': 340},
            ]

            for poke_info in pokemon_data:
                species = PokemonSpecies.objects.get(id=poke_info['species_id'])
                pokemon, created = Pokemon.objects.get_or_create(
                    id=poke_info['id'],
                    defaults={
                        'name': poke_info['name'],
                        'pokemon_species': species,
                        'height': poke_info['height'],
                        'weight': poke_info['weight'],
                        'base_experience': poke_info['base_experience'],
                        'is_default': True,
                        'order': poke_info['id'],
                    }
                )
                if created:
                    self.stdout.write(f"   ✅ Created Pokemon: {pokemon.name}")

            # Create Berries with all required fields
            berries_data = [
                {'id': 1, 'name': 'cheri', 'item_id': 1, 'firmness_id': 2, 'type_id': 10},
                {'id': 2, 'name': 'chesto', 'item_id': 2, 'firmness_id': 3, 'type_id': 11},
                {'id': 3, 'name': 'pecha', 'item_id': 3, 'firmness_id': 2, 'type_id': 13},
                {'id': 4, 'name': 'rawst', 'item_id': 4, 'firmness_id': 3, 'type_id': 12},
                {'id': 5, 'name': 'aspear', 'item_id': 5, 'firmness_id': 3, 'type_id': 15},
            ]

            for berry_info in berries_data:
                item = Item.objects.get(id=berry_info['item_id'])
                firmness = BerryFirmness.objects.get(id=berry_info['firmness_id'])
                gift_type = Type.objects.get(id=berry_info['type_id'])

                berry, created = Berry.objects.get_or_create(
                    id=berry_info['id'],
                    defaults={
                        'name': berry_info['name'],
                        'item': item,
                        'berry_firmness': firmness,
                        'natural_gift_power': 60,
                        'natural_gift_type': gift_type,
                        'size': 20,
                        'max_harvest': 5,
                        'growth_time': 3,
                        'soil_dryness': 15,
                        'smoothness': 25,
                    }
                )
                if created:
                    self.stdout.write(f"   ✅ Created Berry: {berry.name}")

            # Summary
            pokemon_count = Pokemon.objects.count()
            ability_count = Ability.objects.count()
            type_count = Type.objects.count()
            berry_count = Berry.objects.count()

            self.stdout.write(f"\n🎉 Educational data loaded successfully!")
            self.stdout.write(f"📊 Database summary:")
            self.stdout.write(f"   Pokemon: {pokemon_count}")
            self.stdout.write(f"   Abilities: {ability_count}")
            self.stdout.write(f"   Types: {type_count}")
            self.stdout.write(f"   Berries: {berry_count}")

            self.stdout.write(f"\n🔗 Test your educational API endpoints:")
            self.stdout.write(f"   /api/v2/writable-pokemon/")
            self.stdout.write(f"   /api/v2/writable-ability/")
            self.stdout.write(f"   /api/v2/writable-type/")
            self.stdout.write(f"   /api/v2/writable-berry/")

        except Exception as e:
            self.stdout.write(f"❌ Error loading sample data: {e}")
            import traceback
            self.stdout.write(f"Full traceback: {traceback.format_exc()}")
            raise e

        self.stdout.write(f"\n🎓 Educational Pokemon API ready for students!")
