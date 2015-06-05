import requests

# SECRET = 'HiJIvGEzHwyEBhWv4JSnDLDo3h3082Z5srousLdVoQdLxNJBHaYEnT6cMw2EGDT6xSd1BNVSLxOV8E0jiYUfPg775xTtEipxJ9Izx9jOYk4flUO2upNmwwX9M4RE4KRh'
SECRET = 'ozwqgkXlQ9sdLWQcYXHcNGYgXS9FZlb0Jxq3AA7GjPBTrq2fMqh98rtk7jClN8gwx87GlSXTZUHdYIoFpO5DI1IN4PbhtywO9biW9fhVhu4s9XZ9V09hX62pigVm6r1L'
payload = {
    'grant_type': 'password',
    'username': 'pedro',
    'password': 'pedro',
    # 'client_id': 'Q0ANsPj1htggi7hsRj73SyQXUlJmMBY5GbLdVwWR',
    'client_id': '1jFmMYli2nnwt7b56t0yYnidDxgijHW6AnqEt3gi',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('http://localhost:8000/o/token/', payload).text