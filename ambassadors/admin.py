from django.contrib import admin
from ambassadors.models import Ambassador, Merch


@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    list_display = (
        'telegram', 'name', 'onboarding_date', 'notification',
        'ambassador_status', 'ambassador_address', 'profile',
        'content', 'merch', 'promocode', 'comment'
    )
    list_editable = (
        'name', 'onboarding_date', 'notification',
        'ambassador_status', 'ambassador_address', 'profile',
        'content', 'merch', 'promocode', 'comment'
    )


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    """Отображение мерча в админке."""
    list_display = [
        'id',
        'merch_type',
        'category',
        'price'
    ]
    empty_value_display = ' пусто '
