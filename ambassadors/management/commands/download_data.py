import json

from django.core.management.base import BaseCommand

from ambassadors.models import Merch


def clear_data(self):
    Merch.objects.all().delete()
    self.stdout.write(
        self.style.WARNING('Существующие записи мерча были удалены.')
    )

class Command(BaseCommand):
    help = 'Update data merch'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Удаляет предыдущие данные',
        )
    def handle(self, *args, **options):
        """Загрузка данных."""

        if options['delete_existing']:
            clear_data(self)
        with open('ambassadors/data/merch_dump.json', encoding='utf8') as file:
            data = json.load(file)
        for entry in data:
            id = entry.get('id')
            merch_type = entry.get('merch_type')
            category = entry.get('category')
            price = entry.get('price')        

            Merch.objects.get_or_create(
                id=id, merch_type=merch_type,
                category=category, price=price,
            )

        self.stdout.write(
            self.style.SUCCESS('Записи мерча сохранены')
        )
