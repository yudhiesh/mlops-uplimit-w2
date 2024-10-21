import json

import requests


postive_sample_data = {"review": "Hello world this is the best product ever!"}
negative_sample_data = {"review": "I did not like this product."}
neutral_sample_data = {"review": "neutral"}
merged_data = []
merged_data.append(postive_sample_data)
merged_data.append(negative_sample_data)
merged_data.append(neutral_sample_data)

headers = {"Content-Type": "application/json"}
print(merged_data)
for data in merged_data:
    print(data)
    response = requests.post(
         "http://127.0.0.1:8000/predict", data=json.dumps(data), headers=headers
     )
    print(response.status_code, response.json())
