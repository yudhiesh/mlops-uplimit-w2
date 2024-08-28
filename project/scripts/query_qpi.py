import json

import requests

data = {"review": "Hello world this is the best product ever!"}
headers = {"Content-Type": "application/json"}
resp = requests.post(
    "http://127.0.0.1:8000/predict", data=json.dumps(data), headers=headers
)
print(resp.status_code, resp.json())
