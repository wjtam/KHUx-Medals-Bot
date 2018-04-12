import requests

URL = "https://www.khuxbot.com/api/v2/get"
PARAMS = {"format":["name","image_link","tier","direction","element","targets","attack","defense","multipler","notes"],
"filter":{"tier"}:{"min":6}}

r = requests.get(url = URL, params = PARAMS)
data = r.json()

medal = 

print(data)





