import requests

#SECRET = 'ntu7mHezuFj5BPAFgsExi9rlxW5i50mxLfXEk4xojM9f77rE95ekAHKAcmNYlAtSHFoXWtGHEt9IgU0oRtVcfA8vilDUVdHmrB9AUOrd0YTukvGScRQ0c7E6EUyhxDoK'

#payload = {
#    'grant_type': 'password',
#    'username': 'pedro',
#    'password': 'pedro',
#    'client_id': '4y4P7D8w8JkgKPPp8NBYoHESqjXtU7IueNFWk6LG',
#    'client_secret': SECRET,
#    'scope': 'write read'
#}
#print requests.post('http://127.0.0.1:8000/o/token/', payload).text


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