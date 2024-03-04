from django.contrib import admin
from .models import NotificationType, NotificationStatus, Notification


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'slug')
    prepopulated_fields = {'slug': ('type',)}


@admin.register(NotificationStatus)
class NotificationStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'slug')
    prepopulated_fields = {'slug': ('status',)}


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'status', 'ambassador', 'pub_date')
    list_filter = ('type', 'status', 'ambassador')
    search_fields = ('type__type', 'status__status', 'ambassador__username')
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('type', 'status', 'ambassador', 'pub_date')
        }),
    )
