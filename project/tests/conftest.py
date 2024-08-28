import pytest
import ray
from ray import serve

from src.server import APIIngress, SimpleModel

# This file instantiates Ray test fixtures to reuse across multiple tests


@pytest.fixture(scope="session")
def ray_serve():
    try:
        ray.init(
            # Suggested to hard code num_cpus from docs:
            # https://docs.ray.io/en/latest/ray-core/examples/testing-tips.html#tip-1-fixing-the-resource-quantity-with-ray-init-num-cpus
            num_cpus=1,
        )
        yield serve.start(detached=True, http_options={"host": "0.0.0.0"})
    finally:
        ray.shutdown()


@pytest.fixture(scope="session")
def ray_serve_app(ray_serve):
    serve.run(
        APIIngress.options(ray_actor_options={"num_cpus": 0}).bind(
            SimpleModel.options(ray_actor_options={"num_cpus": 0}).bind()
        ),
    )
    yield ray_serve


@pytest.fixture
def predict_url(ray_serve_app):
    return "http://127.0.0.1:8000/predict"
