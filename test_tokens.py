import requests

# SECRET = 'HiJIvGEzHwyEBhWv4JSnDLDo3h3082Z5srousLdVoQdLxNJBHaYEnT6cMw2EGDT6xSd1BNVSLxOV8E0jiYUfPg775xTtEipxJ9Izx9jOYk4flUO2upNmwwX9M4RE4KRh'
SECRET = '32uZTgjlcvx95jXSTBXyz5VDS3BJDqf5zt2k3LGXp9vEuXFlc85ExsMUCrZNn1xKLoOKtddEMoRi60IuryXTwsTUDEAhXo2d8mZHKjpG7kU6bFAwSog1FFgLrEX3QJoI'
payload = {
    'grant_type': 'password',
    'username': 'pedro',
    'password': 'pedro',
    # 'client_id': 'Q0ANsPj1htggi7hsRj73SyQXUlJmMBY5GbLdVwWR',
    'client_id': 'vUUS5McTbLr8LwfbIkGezK184gdcGiPqZ1Du4Ny7',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
# print requests.post('http://localhost:8000/o/token/', payload).text