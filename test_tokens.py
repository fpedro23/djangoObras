import requests

SECRET = 'ijtUJ22aI8z4BrUVmRpVFqGkIJOzTemb4F6lsJG5J8ngqsrgT9kjx0g0sOHr97DZgGiteDs4sB6XBA1OEBYbMF32FYmDIECGrvP7wPeVmH3KOAQBWu7ELbL0XNApTLrO'
payload = {
    'grant_type': 'password',
    'username': 'capusu',
    'password': 'capusu',
    'client_id': 'DHDX7hqj3O4LkNVnt9ks7T13SNlcwiPo7yYMsDw6',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('https://obrasapf.mx/o/token/', payload).text