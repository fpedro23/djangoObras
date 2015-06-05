import requests


SECRET = '1jAcEjCEy2j2fk5V1SJx2lGZeE1LZkEiVRlRUhJrzgRLyDvzWjjCrTHgrB8hVfppObqFgJkPhr1XxvauY9zNRoQcfEnYwXsLj4s5cQlw5PNSZLEuFMQQQYjyrqypuAkv'

payload = {
    'grant_type': 'password',
    'username': 'ags',
    'password': 'ags',
    'client_id': '7qLt3wR97jN42xQyHXBeE8OJ3OojVrIXPkl2H6CV',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text