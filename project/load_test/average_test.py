from locust import HttpUser, task, between
import json

class APIUser(HttpUser):
    wait_time = between(0.5, 1)  # Wait between 0.5 and 1 second between tasks

    @task
    def predict(self):
        headers = {"Content-Type": "application/json"}
        data = {"review": "Hello world this is the best product ever!"}

        with self.client.post("/predict", data=json.dumps(data), headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got unexpected response status code: {response.status_code}")
