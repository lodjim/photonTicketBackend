from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import Person


def verification(request, token):
    try:
        data = Person.objects.get(token=token)
        if data.is_scanned:
            return JsonResponse({"Prenom": data.prenom, "Nom": data.nom, "acces": False})
        else:
            data.is_scanned = True
            data.save()
            return JsonResponse({"Prenom": data.prenom, "Nom": data.nom, "acces": True})
    except:
        pass
    return JsonResponse({"Prenom": "none", "Nom": "none", "acces": False})
