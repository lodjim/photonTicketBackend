from django.db import models

# Create your models here.


class Person(models.Model):
    list_of_filiere = (("GEA","GEA"),("GACT","GACT"),("BTP","BTP"),("GT","GT"),("GEII","GEII"),("GLT","GLT"),("LPGT","LPGT"))
    prenom = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    filiere = models.CharField(max_length=4,choices=list_of_filiere)
    token = models.CharField(max_length=300)
    is_scanned = models.BooleanField(default=False)
    def __str__(self):
        return self.prenom+" "+self.nom
