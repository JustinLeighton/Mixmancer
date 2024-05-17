import requests

url = "http://192.168.0.107:8000/send-data"

data = {
    "d4": 0,
    "d6": 0,
    "d8": 0,
    "d10": 0,
    "d12": 0,
    "d20": 1,
    "d100": 0,
    "modifier": 0,
    "advantage": True,
}
response = requests.post(url, json=data)
print(response.json())
