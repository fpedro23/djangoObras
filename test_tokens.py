import requests

SECRET = 'YEkNe@jlOqaIcHtDmWzW.;SvNVDTDvo4wyLe:nKoKOrIHTcy;cLZ@=A-NATnZq_0BvUML7K@8E?@F2pkR0-_9loY1!-rJQxnm=toHau0GqvBU!pIZ5a;AKt8aV=.d0iP'

payload = {
    'grant_type': 'password',
    'username': 'pedro',
    'password': 'pedro',
    'client_id': '.BWRdbZrL7sDx=VYpKaLnijuh1bH.tBAzpz.mT2z',
    'client_secret': SECRET,
    'scope': 'write read'
}
print requests.post('http://localhost:8000/o/token/', payload).text
