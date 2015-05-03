import requests

SECRET = 'uRdI2v2nOxq0iIvoPnJGQuNorLwhYS4NyynuByZJtQq9MZXwXRVmfvx6JBwYUojjQBAjqoTfacgREDadJDfoLoF7TPV6JJmsx2q855INlWsBapzZzKhikYP3EXDNdFT7'

payload = {
    'grant_type': 'password',
    'username': 'ags',
    'password': 'ags',
    'client_id': 'IZouS8x2DexzbwHifHWR499NNgsIMIggbbbJ3lkt',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text
