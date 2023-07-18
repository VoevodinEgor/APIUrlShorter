import requests

resp = requests.post(
    'http://localhost:8001/shorts', json={'url': 'https://google.com'}
)

print(resp.status_code)
print(resp.raw)
print(resp.text)
try:
    print(resp.json())
except Exception:
    print('Not valid JSON')
url = resp.json()['url']
resp = requests.get(
    f'http://localhost:8001/shorts/{url}'
)
print(resp.status_code)
print(resp.raw)
print(resp.text)
try:
    print(resp.json())
except Exception:
    print('Not valid Json')