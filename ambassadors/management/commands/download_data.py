import json

from django.core.management.base import BaseCommand

from ambassadors.models import Merch, Content, Ambassador, Address, Profile


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

        with open('ambassadors/data/ambassadors_dump.json', encoding='utf8') as file:
            data = json.load(file)

        for entry in data:
            # Extract ambassador data
            pub_date = entry.get('pub_date')
            telegram = entry.get('telegram')
            name = entry.get('name')

            # Extract profile data
            profile_data = entry.get('profile')
            email = profile_data.get('email')
            gender = profile_data.get('gender')
            job = profile_data.get('job')
            clothing_size = profile_data.get('clothing_size')
            foot_size = profile_data.get('foot_size')
            blog_link = profile_data.get('blog_link')
            additional = profile_data.get('additional')
            education = profile_data.get('education')
            education_path = profile_data.get('education_path')
            education_goal = profile_data.get('education_goal')
            phone = profile_data.get('phone')
            birth_date = profile_data.get('birth_date')

            address_data = entry.get('address')
            country = address_data.get('country')
            region = address_data.get('region')
            city = address_data.get('city')
            address = address_data.get('address')
            postal_code = address_data.get('postal_code')

            content_data = entry.get('content')
            link = content_data.get('link')
            date = content_data.get('date')
            guide_condition = content_data.get('guide_condition')

            status = entry.get('status')
            comment = entry.get('comment')
            guide_status = entry.get('guide_status')
            address = Address.objects.create(
                    country=country,
                    region=region,
                    city=city,
                    address=address,
                    postal_code=postal_code
                )
            profile = Profile.objects.create(
                    email=email,
                    gender=gender,
                    job=job,
                    clothing_size=clothing_size,
                    foot_size=foot_size,
                    blog_link=blog_link,
                    additional=additional,
                    education=education,
                    education_path=education_path,
                    education_goal=education_goal,
                    phone=phone,
                )
            ambassador, created = Ambassador.objects.get_or_create(
                telegram=telegram,
                defaults={
                    'pub_date': pub_date,
                    'name': name,
                    'status': status,
                    'comment': comment,
                    'guide_status': guide_status,
                    'address': address,
                    'profile': profile,
                }
            )

            if created:
                Content.objects.create(
                    ambassador=ambassador,
                    link=link,
                    date=date,
                    guide_condition=guide_condition
                )

        self.stdout.write(
            self.style.SUCCESS('Записи амбассадоров сохранены.')
        )
