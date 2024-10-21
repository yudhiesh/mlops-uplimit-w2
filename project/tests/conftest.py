import pytest
import ray
from ray import serve

from src.server import APIIngress, SimpleModel

# This file defines pytest fixtures for Ray Serve, which can be reused across multiple tests

# Note on fixture order:
# Pytest manages the order of fixture execution based on dependencies.
# Fixtures are executed in the order they are requested by tests or other fixtures.
# In this file, the order of execution will be:
# 1. ray_serve (session scope)
# 2. ray_serve_app (session scope, depends on ray_serve)
# 3. predict_url (function scope, depends on ray_serve_app)
# This ensures that Ray is initialized before the app is deployed,
# and the app is deployed before the URL is provided.

# Define a session-scoped fixture for Ray Serve
@pytest.fixture(scope="session")
def ray_serve():
    try:
        # Initialize Ray with a fixed number of CPUs
        ray.init(
            # Hardcoding num_cpus is recommended for consistent test environments
            # https://docs.ray.io/en/latest/ray-core/examples/testing-tips.html#tip-1-fixing-the-resource-quantity-with-ray-init-num-cpus
            num_cpus=1,
        )
        # Start Ray Serve in detached mode, binding it to all network interfaces
        yield serve.start(detached=True, http_options={"host": "0.0.0.0"})
    finally:
        # Ensure Ray is shut down after all tests are complete
        ray.shutdown()

# Define a session-scoped fixture for the Ray Serve application
@pytest.fixture(scope="session")
def ray_serve_app(ray_serve):
    # Deploy the application using Ray Serve
    serve.run(
        # Create an APIIngress instance, setting CPU allocation to 0
        APIIngress.options(ray_actor_options={"num_cpus": 0}).bind(
            # Create a SimpleModel instance, also setting CPU allocation to 0
            SimpleModel.options(ray_actor_options={"num_cpus": 0}).bind()
        ),
    )
    # Yield the Ray Serve instance for use in tests
    yield ray_serve

# Define a function-scoped fixture for the prediction URL
@pytest.fixture
def predict_url(ray_serve_app):
    # Return the URL for the prediction endpoint
    return "http://127.0.0.1:8000/predict"