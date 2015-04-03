import requests

payload = {
    'id': 'password',

}
print requests.post('http://127.0.0.1:8000/obras/api/buscarObras', payload).text
