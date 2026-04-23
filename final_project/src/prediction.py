import http.client
import requests

# conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")

headers = {
    'x-apisports-key': "F7gHQGrguyeXngQrKE5LsD41iB6MeELl" #find a way to not hardcode this
    }

# conn.request("GET", "/leagues", headers=headers)
response = requests.get(("v1.american-football.api-sports.io", "/leagues", headers=headers))

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

print(response)