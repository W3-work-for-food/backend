from django.contrib import admin
from ambassadors.models import Ambassador, Merch, Address, Promocode, Profile


class PromocodeInline(admin.TabularInline):
    model = Promocode


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
        'guide_status'
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
    list_display = [
        'id',
        'merch_type',
        'category',
        'price'
    ]
    empty_value_display = ' пусто '
