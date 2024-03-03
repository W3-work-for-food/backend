from django.db import models

from django.contrib.auth import get_user_model

Ambassador = get_user_model()


class AmbassadorProfile(models.Model):
    user = models.OneToOneField(Ambassador, on_delete=models.CASCADE)
