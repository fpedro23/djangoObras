import requests

# SECRET = 'HiJIvGEzHwyEBhWv4JSnDLDo3h3082Z5srousLdVoQdLxNJBHaYEnT6cMw2EGDT6xSd1BNVSLxOV8E0jiYUfPg775xTtEipxJ9Izx9jOYk4flUO2upNmwwX9M4RE4KRh'
SECRET = 'N31kf1adaycNFSlL7aacVf5GkiXrFLSzb7Dv9cPV92k8oEluqW7VCPYXigX21mmtozdbT2CAo2jQMLT5tpNudv8MESYWqFwtbZ1W8h79Elu8irbiyjeHuwQymojZ3jkq'
payload = {
    'grant_type': 'password',
    'username': 'superuser',
    'password': 'superuser',
    # 'client_id': 'Q0ANsPj1htggi7hsRj73SyQXUlJmMBY5GbLdVwWR',
    'client_id': 'gAxfAeUaXVxyL6Wm2P2wbKDucc9JtHfYWTq2nIrz',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('http://localhost:8000/o/token/', payload).text