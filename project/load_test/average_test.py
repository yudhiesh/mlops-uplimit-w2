from locust import HttpUser, task, between
import json

class APIUser(HttpUser):
    # Define the wait time between tasks for each simulated user
    # Users will wait randomly between 0.5 and 1 second after each task
    wait_time = between(0.5, 1)

    @task
    def predict(self):
        headers = {"Content-Type": "application/json"}
        data = {"review": "Hello world this is the best product ever!"}

        # Send a POST request to the '/predict' endpoint
        with self.client.post("/predict",
                              data=json.dumps(data),  # Convert data to JSON string
                              headers=headers,
                              catch_response=True  # This allows us to mark the response as success or failure
                             ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got unexpected response status code: {response.status_code}")

# Note: This script defines the behavior for simulated users, but doesn't actually run the load test
# To run the test, you need to execute this script with Locust command-line tool