import requests

SECRET = 'Byr8I8CTKVSVtw0lPLQz03ljL2d2fwPKW23dEUylv2ofEtPZ6oFbvEQh5SGnp76rjrY8dedmvDWaOjOp1mwZfbxy893ouARVIlqMP8eaXdem07A0AwswSzBFsu1zXuOC'

payload = {
    'grant_type': 'password',
    'username': 'ags',
    'password': 'ags',
    'client_id': 'U5YLz9L5QNnZ7llan3YW9I6za0mQp8YWozWAsRO6',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text