from django.contrib import admin

from ambassadors.models import (Address, Ambassador, Content, Merch, Profile,
                                Promocode, SentMerch)
from ambassadors.models import Notification


class PromocodeInline(admin.TabularInline):
    model = Promocode


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'status', 'ambassador')
    list_filter = ('type', 'status', 'ambassador')
    date_hierarchy = 'pub_date'
    exclude = ('pub_date',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'country',
        'city',
        'address',
        'postal_code'
    ]
    empty_value_display = ' пусто '


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'promocode',
        'is_active'
    ]
    empty_value_display = ' пусто '


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'gender',
        'job',
        'clothing_size',
        'foot_size',
        'blog_link',
        'additional',
        'education',
        'education_path',
        'education_goal',
        'phone'
    ]
    empty_value_display = ' пусто '


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'date', 'guide_condition')
    search_fields = ('link',)
    list_filter = ('guide_condition',)


@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    inlines = [
        PromocodeInline,
    ]
    list_display = (

        'id',
        'pub_date',
        'telegram',
        'name',
        'address',
        'profile',
        'promocodes',
        'comment',
        'guide_status',
        'status'
    )
    list_editable = (
         'telegram',
         'name',
         'address',
         'profile',
         'comment',
         'guide_status'
    )

    def promocodes(self, obj):
        return obj.promocodes.all()

    promocodes.short_description = 'Промокоды'


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    """Отображение мерча в админке."""
    list_display = (
        'id',
        'merch_type',
        'category',
        'price'
    )
    empty_value_display = ' пусто '


@admin.register(SentMerch)
class SentMerchAdmin(admin.ModelAdmin):
    """Отображение отправки мерча в админке."""
    list_display = (
        'id',
        'user',
        'ambassador',
        'date',
    )
