
import sys
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
import requests
import json
import pprint
import datetime
import md5

import hashlib



hoy = datetime.date.today()
ahora = datetime.datetime.now()
h = int(ahora.hour)%12
d = int(hoy.day)
m = int(hoy.month)
a = int(str(hoy.year)[2:])

print "year: ", a
print "month: ", m
print "day: ", d
print "hour: ", h

token_prefix = d*3 + m*2702 + a*612 + h*2601

token = str(token_prefix) +  "Xt1V3r1f1c4U5u4r10"

md5_token = hashlib.md5(token).hexdigest()

print "token md5: ", md5_token



headers = {'Content-type': 'application/x-www-form-urlencoded', "Accept": "text/plain"}



parametros = {'username': 'pruebatra', 'password': 'passxti', 'token': md5_token}


r = requests.post('http://ginxti.com/WebServices/verificaUsuario/verificaUsuario.php', data=parametros)

respuesta = json.loads(r.content)

r_activo = respuesta["activo"]
r_error = respuesta["error"]


print respuesta


