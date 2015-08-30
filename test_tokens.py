import requests

SECRET = '8bpPEU9waiyt79ktFGCx37neGuFzoxR8mwZOZCEBB4gMUw5Z0YmNOlBeUil38FubU79NAJXYUO509mFx5Ok5vQkeqYcOBmtH5pCxZWtOaKyL8x9CBsNlbDZAEucqdBZ1'
payload = {
    'grant_type': 'password',
    'username': 'fcabeza',
    'password': 'fcabeza',
    'client_id': 'S4RxljlRMQnTcdeTxHo7QEgJCDjdBOroXZ14Eeej',
    'client_secret': SECRET,
    'scope': 'write read'
}
# print requests.post('http://edicomex.com.mx:7500/o/token/', payload).text
print requests.post('https://obrasapf.mx/o/token/', payload).text