from fastapi import FastAPI
from ray import serve
from ray.serve.handle import DeploymentHandle
from loguru import logger
import sys
from src.data_models import SimpleModelRequest, SimpleModelResponse, SimpleModelResults
from src.model import Model

app = FastAPI(
    title="Drug Review Sentiment Analysis",
    description="Drug Review Sentiment Classifier",
    version="0.1",
)

# TODO: Add in appropriate logging using loguru wherever you see fit
# in order to aid with debugging issues.
logger.add(sys.stderr, format="{time} - {name} - {level} - {message}")

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
        print(f"Req for predict : {request}")
        logger.info(f"Request for predict - {request}")
        try:
            result = await self.handle.predict.remote(request.review)
            print(f"Prediction result: {result}")
            return SimpleModelResponse.model_validate(result.model_dump())
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            raise e



@serve.deployment(
    ray_actor_options={"num_cpus": 0.2},
    autoscaling_config={"min_replicas": 1, "max_replicas": 2},
)
class SimpleModel:
    def __init__(self) -> None:
        self.session = Model.load_model()

    def predict(self, review: str) -> SimpleModelResults:
        # TODO: Use the Model.predict to get the result
        #logger.info(f"review str to score {review}")
        try:
            result = Model.predict(self.session, review)
            logger.info(f"Prediction : {result}")
            return SimpleModelResults.model_validate(result)
        except Exception as e:
            logger.error(f"Error in model prediction: {str(e)}")
            raise e


entrypoint = APIIngress.bind(
    SimpleModel.bind(),
)
