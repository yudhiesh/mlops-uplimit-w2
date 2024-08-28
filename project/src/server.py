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


@serve.deployment(num_replicas=1)
@serve.ingress(app)
class APIIngress:
    def __init__(self, simple_model_handle: DeploymentHandle) -> None:
        self.handle = simple_model_handle

    @app.post("/predict")
    async def predict(self, request: SimpleModelRequest):
        results = await self.handle.predict.remote(request.review)
        return SimpleModelRespone.model_validate(results.model_dump())


@serve.deployment(
    ray_actor_options={"num_cpus": 1},
    autoscaling_config={"min_replicas": 1, "max_replicas": 2},
)
class SimpleModel:
    def __init__(self) -> None:
        self.session = Model.load_model()

    def predict(self, review: str) -> SimpleModelResults:
        results = Model.predict(self.session, review=review)
        return SimpleModelResults.model_validate(results)


entrypoint = APIIngress.bind(SimpleModel.bind())
