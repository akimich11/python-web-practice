import requests
import base64


requests.post('https://datasend.webpython.graders.eldf.ru/submissions/1/', headers={'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}).json()

requests.put('https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/', headers={'Authorization': ('Basic ' + base64.b64encode("alibaba:40razboinikov".encode('utf-8')).decode('utf-8'))}).json()

