import requests


payload = {
    'access_token': 'KdJ8I915OEpz4hDkyZ85RHWwYrPC8I',
}
print requests.get('http://localhost:8000/obras/api/dependencias?access_token=KdJ8I915OEpz4hDkyZ85RHWwYrPC8I').text
