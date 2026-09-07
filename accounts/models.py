from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    job_title = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.username