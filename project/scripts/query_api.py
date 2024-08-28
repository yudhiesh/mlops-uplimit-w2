import json

import requests

data = {"review": "Hello world this is the best product ever!"}
headers = {"Content-Type": "application/json"}
response = requests.post(
    "http://127.0.0.1:8000/predict", data=json.dumps(data), headers=headers
)
print(response.status_code, response.json())
