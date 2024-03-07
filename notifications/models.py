from django.db import models

from ambassadors.models import Ambassador


class NotificationType(models.Model):
    class Types(models.TextChoices):
        NEW_PROFILE = 'Новая анкета'
        NEW_CONTENT = 'Новый контент'
        GUIDE_COMPLETED = 'Гайд выполнен'

    slug = models.SlugField(unique=True)
    type = models.CharField(
        max_length=20,
        choices=Types.choices,
        default=Types.NEW_PROFILE
    )

    class Meta:
        verbose_name = 'Тип уведомления'
        verbose_name_plural = 'Типы уведомлений'

    def __str__(self):
        return self.type


class NotificationStatus(models.Model):
    class Statuses(models.TextChoices):
        READ = 'Прочитано'
        UNREAD = 'Непрочитано'

    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=Statuses.choices,
        default=Statuses.UNREAD
    )

    class Meta:
        verbose_name = 'Статус уведомления'
        verbose_name_plural = 'Статусы уведомлений'

    def __str__(self):
        return self.status


class Notification(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    ambassador = models.ForeignKey(
        Ambassador,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        NotificationType,
        related_name='types',
        on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        NotificationStatus,
        related_name='statuses',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.type} - {self.status}'
