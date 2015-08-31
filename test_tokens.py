import requests

SECRET = 'Ito4EuoY5hhWuOynPlOxJkgiAguO2tHpFsIZHgkh6HMjN4gHLsOdbOmHxMitMAdJs9FoJS5lK9DiVIiurS6CeocgCVgKHR6JEBt69HY1nsWXaE1bFA7ZpjNQLbrhlgpf'
payload = {
    'grant_type': 'password',
    'username': 'fcabeza',
    'password': 'fcabeza',
    'client_id': 'nJKmO290WGy5TY4GAmxK23cg8mgTDaYf9bgfE5Mx',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('https://obrasapf.mx/o/token/', payload).text