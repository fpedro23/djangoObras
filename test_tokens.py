import requests

SECRET = 'ntu7mHezuFj5BPAFgsExi9rlxW5i50mxLfXEk4xojM9f77rE95ekAHKAcmNYlAtSHFoXWtGHEt9IgU0oRtVcfA8vilDUVdHmrB9AUOrd0YTukvGScRQ0c7E6EUyhxDoK'

payload = {
    'grant_type': 'password',
    'username': 'pedro',
    'password': 'pedro',
    'client_id': '4y4P7D8w8JkgKPPp8NBYoHESqjXtU7IueNFWk6LG',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text
