import requests

# SECRET = 'HiJIvGEzHwyEBhWv4JSnDLDo3h3082Z5srousLdVoQdLxNJBHaYEnT6cMw2EGDT6xSd1BNVSLxOV8E0jiYUfPg775xTtEipxJ9Izx9jOYk4flUO2upNmwwX9M4RE4KRh'
SECRET = 'Q5hEGs5CjYfYOJH0mvl0V5TZJQpqelQ8AfkAEfSPZisOTXIhE5fIH1snrq39G7dcJmwjkBYWtJwRI7xnyFrNcOLSqm6qOoGkRXN2eiceeZIESb9rzLvfJpQlptn91GaW'
payload = {
    'grant_type': 'password',
    'username': 'a',
    'password': 'a',
    # 'client_id': 'Q0ANsPj1htggi7hsRj73SyQXUlJmMBY5GbLdVwWR',
    'client_id': '5cfJw0evDoM2sDnm4EiIXaDREpy6QC01YKcRIQPw',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('http://localhost:8000/o/token/', payload).text