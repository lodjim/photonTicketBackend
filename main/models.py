from django.db import models

# Create your models here.


class Person(models.Model):
    prenom = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    token = models.CharField(max_length=300)
    is_scanned = models.BooleanField(default=False)
