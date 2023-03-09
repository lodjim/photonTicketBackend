from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import hashlib
import qrcode
import numpy as np
import cv2
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Person
import uuid
@login_required(login_url='/login/')
def homepage(request):
    return render(request,"main/index.html")

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

@login_required(login_url='/login/')
def create_ticket(request):
    if request.method =="POST":
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        filiere = request.POST.get('filiere')
        tok = str(uuid.uuid1())
        data = {'prenom': prenom,
        "nom": nom,
        "filiere":filiere,
        "uuid": tok
        }
        
        if prenom.isspace() or nom.isspace() or filiere.isspace():
            return JsonResponse({"status":"error"})
        else:
            data_str = json.dumps(data)
            token = hashlib.sha256(data_str.encode('utf8')).hexdigest()
            path = f"/static/{prenom}-{nom}-{filiere}-{token}.png"
            instance = Person(prenom=prenom,nom=nom,token=token)
            instance.save()
            img = qrcode.make(token)
            img_array = np.array(img.convert("RGB"))
            img_src = cv2.imread("./static/template.png")
            h_src, w_src, _ = img_src.shape
            h_qr, w_qr, _ = img_array.shape
            img_src[10:h_qr+10, w_src-w_qr-10:w_src-10] = img_array
            cv2.imwrite(f"./static/{prenom}-{nom}-{filiere}-{token}.png",img_src)
            return render(request,"main/creation.html",{'path_img':path,'prenom':prenom,'nom':nom,'filiere':filiere})
    return JsonResponse({"status":"THIS REQUEST IS NOT ALLOWED"})


def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            return render(request,"main/login.html")
    
    return render(request,"main/login.html")