import requests

SECRET = 'vzqsAZ7y4oiWfvRiRBiGVJn0ei9iFXmXe0xBBQt4jNCAvgg7VaIRS3XDslKoVi3jLiV8iQwcKybHqbdSGmPU8Qo51rXf2yCP4rItKJ9DyxFtDhyU1r4SbvY72iw85QjG'

payload = {
    'grant_type': 'password',
    'username': 'pedro',
    'password': 'pedro',
    'client_id': 'hT5YkoknQRIWkF5Kxrq0kUN06IyI8YimSjlHpuJJ',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text
