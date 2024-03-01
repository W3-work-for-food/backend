from django.db import models


class AmbassadorStatus(models.Model):
    slug = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class Content(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    link = models.URLField(max_length=255, unique=False, blank=False)
    date = models.DateTimeField(
        max_length=30,
        auto_now_add=True,
        unique=False,
        blank=False
    )
    guide_condition = models.BooleanField(unique=False, blank=False)
