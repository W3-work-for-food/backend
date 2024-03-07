import json

from django.core.management.base import BaseCommand

from users.models import User


def clear_data(self):
    User.objects.all().delete()
    self.stdout.write(
        self.style.WARNING('Существующие записи пользователей были удалены.')
    )


class Command(BaseCommand):
    help = 'Update data user'

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
        with open('ambassadors/data/users_dump.json', encoding='utf8') as file:
            data = json.load(file)
        for entry in data:
            id = entry.get('id')
            email = entry.get('email')
            first_name = entry.get('first_name')
            username = entry.get('username')        
            last_name = entry.get('last_name')        
            password = entry.get('password')        

            User.objects.get_or_create(
                id=id, email=email,
                first_name=first_name,
                username=username,
                last_name=last_name,
                password=password,
            )

        self.stdout.write(
            self.style.SUCCESS('Записи пользователей сохранены')
        )
