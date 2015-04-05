import requests

SECRET = 'vzqsAZ7y4oiWfvRiRBiGVJn0ei9iFXmXe0xBBQt4jNCAvgg7VaIRS3XDslKoVi3jLiV8iQwcKybHqbdSGmPU8Qo51rXf2yCP4rItKJ9DyxFtDhyU1r4SbvY72iw85QjG'

payload = {
    'access_token': 'JgC2EPWmeRwzqzLrPn42jJKZ3dI1qN',
}
print requests.post('http://localhost:8000/users/', payload).text
