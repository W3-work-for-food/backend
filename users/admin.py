from django.contrib import admin
from .models import User

@admin.register(User)
class MerchAdmin(admin.ModelAdmin):
    """Отображение пользователей в админке."""
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'password'
    ]
    empty_value_display = ' пусто '