from django.contrib import admin
from .models import Merch


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