from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    country = CountryField(blank_label='(select country)')
    profile_pic_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.email
