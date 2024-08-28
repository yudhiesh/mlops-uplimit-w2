from fastapi import FastAPI
from ray import serve
from ray.serve.handle import DeploymentHandle

from src.data_models import SimpleModelRequest, SimpleModelRespone, SimpleModelResults
from src.model import Model

app = FastAPI(
    title="Drug Review Sentiment Analysis",
    description="Drug Review Sentiment Classifier",
    version="0.1",
)

# TODO: Add in appropriate logging using loguru wherever you see fit
# in order to aid with debugging issues.


@serve.deployment(
    ray_actor_options={"num_cpus": 0.2},
    autoscaling_config={"min_replicas": 1, "max_replicas": 2},
)
@serve.ingress(app)
class APIIngress:
    def __init__(self, simple_model_handle: DeploymentHandle) -> None:
        self.handle = simple_model_handle

    @app.post("/predict")
    async def predict(self, request: SimpleModelRequest):
        # TODO: Use the handle.predict which is a remote function
        # to get the result
        return SimpleModelRespone.model_validate(result.model_dump())


@serve.deployment(
    ray_actor_options={"num_cpus": 0.2},
    autoscaling_config={"min_replicas": 1, "max_replicas": 2},
)
class SimpleModel:
    def __init__(self) -> None:
        self.session = Model.load_model()

    def predict(self, review: str) -> SimpleModelResults:
        # TODO: Use the Model.predict to get the result
        return SimpleModelResults.model_validate(result)


entrypoint = APIIngress.bind(
    SimpleModel.bind(),
)
