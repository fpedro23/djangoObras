import requests

# SECRET = 'HiJIvGEzHwyEBhWv4JSnDLDo3h3082Z5srousLdVoQdLxNJBHaYEnT6cMw2EGDT6xSd1BNVSLxOV8E0jiYUfPg775xTtEipxJ9Izx9jOYk4flUO2upNmwwX9M4RE4KRh'
SECRET = 'rVuFi5PDOhFrXusRUARRpagCN65IofstPCFVaYwqZ2bapxJTXID1GzDL8DMGOJ62DXw3Ou2eguCnBo1PToOy7bOBokKMbysHc6l75Oob9vyLnJnj2skR0R3ovvcisj0J'
payload = {
    'grant_type': 'password',
    'username': 'pedro',
    'password': 'pedro',
    # 'client_id': 'Q0ANsPj1htggi7hsRj73SyQXUlJmMBY5GbLdVwWR',
    'client_id': '1wywc8qNd800NGm8OcvzhqwtIK18P1IoyO1N7s4r',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('http://localhost:8000/o/token/', payload).text