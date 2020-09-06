from django.db import models
from django.contrib.auth.models import User


class Search(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_search = models.DateTimeField(blank=True, null=True)
    found_surnames = models.CharField(blank=True, default='', max_length=200)


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Surname(models.Model):
    surname = models.CharField(max_length=200)