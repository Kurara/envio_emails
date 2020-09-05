from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Surname(models.Model):
    surname = models.CharField(max_length=200)