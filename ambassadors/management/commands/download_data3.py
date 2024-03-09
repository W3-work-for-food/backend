import json

from django.core.management.base import BaseCommand
from users.models import User  # Import User model

from ambassadors.models import Ambassador, Address, Profile, Content


def clear_data(self):
    Ambassador.objects.all().delete()
    Address.objects.all().delete()
    Profile.objects.all().delete()
    Content.objects.all().delete()
    self.stdout.write(
        self.style.WARNING('Existing Ambassador data was deleted.')
    )


class Command(BaseCommand):

    help = 'Loads Ambassador data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Deletes existing Ambassador data before loading new data.'
        )

    def handle(self, *args, **options):
        if options['delete_existing']:
            clear_data(self)

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

            # Extract address data
            address_data = entry.get('address')
            country = address_data.get('country')
            region = address_data.get('region')
            city = address_data.get('city')
            address = address_data.get('address')
            postal_code = address_data.get('postal_code')

            # Extract content data
            content_data = entry.get('content')
            link = content_data.get('link')
            date = content_data.get('date')
            guide_condition = content_data.get('guide_condition')

            # Extract remaining ambassador data
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
            # Create Ambassador object
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


            # Create Content object if ambassador is created
            if created:
                Content.objects.create(
                    ambassador=ambassador,
                    link=link,
                    date=date,
                    guide_condition=guide_condition
                )

        self.stdout.write(
            self.style.SUCCESS('Ambassador data loaded successfully.')
        )
