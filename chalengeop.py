import requests

url = "https://api.mercadolibre.com/oauth/token"

payload={'grant_type': 'authorization_code',
'client_id': '1562860169862020',
'client_secret': 'yFOwOq0d6dWx5IcgTs0rMLHpgBSegGLw',
'code': 'TG-624b627ac15b8f001cfe88bf-325036294',
'redirect_uri': 'https://challengeop.herokuapp.com/'}
files=[

]
headers = {
  'accept': 'application/json',
  'content-type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
