import http.client
import requests
import json

url = "https://v1.american-football.api-sports.io/teams?id=32" #1-32

payload={}

headers = {
  'x-apisports-key': 'fd6fbe35c28ce3526d4bb21d4d5246ba',
}

response = requests.request("GET", url,headers=headers, data=payload)
response = response.json()
print(f"id = 32: {response['response'][0]['name']}")

# want to loop through it 32 times to get all the teams and maybe cache them probably not tho

# print(response['response'][0]['established']) #gives you the year in which a team was established
# for i in range(0,10):
#     url = (f"https://v1.american-football.api-sports.io/teams?id={i}")
#     response = requests.request("GET", url,headers=headers, data=payload)
    