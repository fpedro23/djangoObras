import requests

SECRET = '672ObBg3mDVzCPzFehZfqoaipoNu9vgpimaF1cIJlXSbXDz5Cr5Q54nx5dexdnC4xkenSrEm4XxKmpdtJQbNNvZS561DtSidxDT4QZ4RpU8jD7XJpNyd0FcuxmvtWV39'

payload = {
    'grant_type': 'password',
    'username': 'ags',
    'password': 'ags',
    'client_id': '9MEWAS20m9XfuDaWXLvS1htdXjUysPwpWLK2WeHb',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text