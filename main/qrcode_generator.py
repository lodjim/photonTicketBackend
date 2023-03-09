import qrcode
import json
import hashlib
#from main.models import Person
import uuid
prenom = 'Djim Momar'

nom = 'Lo'
tok = str(uuid.uuid1())
data = {'prenom': prenom,
        "nom": nom,
        "uuid": tok
        }

data_str = json.dumps(data)
token = hashlib.sha256(data_str.encode('utf8')).hexdigest()
print(token)
"""instance = Person(prenom=prenom,nom=nom,token=token)
instance.save()"""
img = qrcode.make(token)
img.save(f"{prenom}-{nom}-{tok}.png")
