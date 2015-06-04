import requests


SECRET = '1JXqeFguf0067xCikRp9tEe0xA19aKqhPxgCOE4u1n9lwLT20qr6sldy0QuPn3JmE72B5Lgaz7EjnAwb1omFDsWJXUzP5GAw2tgfarhBcwTWyWXAjrADMpYtrSZMhLjj'

payload = {
    'grant_type': 'password',
    'username': 'ags',
    'password': 'ags',
    'client_id': 'iFwBOhpqO5BC2spDEQp00rrxqzTfqxEGqCyRqiM4',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text