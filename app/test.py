import requests
from pprint import pprint

params = {
    "query": "macbook",
    "limit": 50,
    "display": "list",
    "location": "Kazan",
    "searchRadius": 100,
    "lastStamp": 1610905380,
    "key": "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir",
}

resp = requests.get("https://m.avito.ru/api/9/items", params=params).json()
pprint(resp)
