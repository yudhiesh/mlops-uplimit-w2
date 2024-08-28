import numpy as np
import onnxruntime as rt

import wandb
from src.constants import WANDB_API_KEY, WANDB_MODEL_REGISTRY_MODEL_NAME


class Model:
    @classmethod
    def load_model(cls) -> rt.InferenceSession:
        if WANDB_API_KEY is None:
            raise ValueError(
                "WANDB_API_KEY not set, unable to pull the model!",
            )
        run = wandb.init()
        downloaded_model_path = run.use_model(
            name=WANDB_MODEL_REGISTRY_MODEL_NAME,
        )
        return rt.InferenceSession(
            downloaded_model_path, providers=["CPUExecutionProvider"]
        )

    @classmethod
    def predict(
        cls, session: rt.InferenceSession, review: str
    ) -> dict[
        int,
        float,
    ]:
        input_name = session.get_inputs()[0].name
        _, probas = session.run(None, {input_name: np.array([[review]])})
        return probas[0]
