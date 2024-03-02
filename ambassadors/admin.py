from django.contrib import admin
from .models import AmbassadorStatus, Content


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