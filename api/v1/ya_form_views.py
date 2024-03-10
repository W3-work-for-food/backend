from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ambassadors.models import (
    Address, Ambassador, Content, Profile, Notification
)
from .views import AMBASSADORS_DESCRIPTION


@extend_schema(tags=['Амбассадоры'], description=AMBASSADORS_DESCRIPTION)
@api_view(['POST'])
@permission_classes([AllowAny,])
def ambassadors_form_get(request):
    """
    Добавление амбассадоров через яндекс форму.
    """
    try:
        data = request.data
        # Профайл
        profile_data = data['profile']
        email = profile_data['email']
        gender = profile_data['gender']
        job = profile_data['job']
        clothing_size = profile_data['clothing_size']
        foot_size = profile_data['foot_size']
        blog_link = profile_data['blog_link']
        additional = profile_data['additional']
        education = profile_data['education']
        education_path = profile_data['education_path']
        education_goal = profile_data['education_goal']
        phone = profile_data['phone']
        profile = Profile.objects.get_or_create(
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
        address_data = data['address']
        country = address_data['country']
        region = address_data['region']
        city = address_data['city']
        address = address_data['address']
        postal_code = int(address_data['postal_code'])
        address = Address.objects.get_or_create(
            country=country,
            region=region,
            city=city,
            address=address,
            postal_code=postal_code
        )

        telegram = data['telegram']
        name = data['name']
        pub_date = datetime.now()
        status = data['status']
        comment = data['comment']
        guide_status = data['guide_status']
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
            Notification.objects.create(
                ambassador=ambassador, type='new_profile',
                status='unread'
            )
        Content.objects.create(
            ambassador_id=ambassador.id,
        )
    except:
        raise TypeError('Неверный данные')

    return Response(status=HTTP_201_CREATED)
