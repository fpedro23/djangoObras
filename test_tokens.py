import requests

SECRET = '5K7TIczTuazzwEY5t6qmWItNoqFQNimzgGQbOpR1Y9q9Pe9iamP4gnT6FI7TUlfuZoSEhZ4BdGSngwb7tqOhHmwv497ExPUSsI2BT8vRhcXWD5FLzPgHvMHh7AXVJI6y'
payload = {
    'grant_type': 'password',
    'username': '',
    'password': 'capusu',
    'client_id': '2GNk4k1QcEPlMmXidG2nFshqvn1Eu8Y0P6t26DC6',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('https://obrasapf.mx/o/token/', payload).text
# capusu b9Ym8wLVzVkiJDxXAhDFsxpbjdvy1O
# ags 1IPGDU8ZCDdaqku7XG1VdHsrxvgsNN