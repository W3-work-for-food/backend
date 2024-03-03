from django.contrib import admin

from ambassadors.models import Ambassador, Merch, AmbassadorStatus, Content


@admin.register(AmbassadorStatus)
class AmbassadorStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'status')
    search_fields = ('slug', 'status')
    list_filter = ('status',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'date', 'guide_condition')
    search_fields = ('link',)
    list_filter = ('guide_condition',)


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
    list_display = (
        'id',
        'merch_type',
        'category',
        'price'
    )
    empty_value_display = ' пусто '
