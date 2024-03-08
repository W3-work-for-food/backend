from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUser(admin.ModelAdmin):
    """Отображение пользователей в админке."""
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
    ]
    empty_value_display = ' пусто '