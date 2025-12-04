from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drop and recreate database tables for clean migration'

    def handle(self, *args, **options):
        self.stdout.write("🗄️ Dropping existing tables for clean migration...")

        with connection.cursor() as cursor:
            # Drop existing tables if they exist
            tables_to_drop = [
                'pokemon_v2_berry',
                'pokemon_v2_pokemon',
                'pokemon_v2_pokemonspecies',
                'pokemon_v2_ability',
                'pokemon_v2_type',
                'pokemon_v2_item',
                'pokemon_v2_itemcategory',
                'pokemon_v2_itempocket',
                'pokemon_v2_berryfirmness'
            ]

            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    self.stdout.write(f"   ✅ Dropped table: {table}")
                except Exception as e:
                    self.stdout.write(f"   ⚠️  Could not drop {table}: {e}")

        self.stdout.write("🎉 Database cleaned! Ready for proper migrations.")
