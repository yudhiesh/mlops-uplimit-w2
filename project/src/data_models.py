from pydantic import BaseModel, ConfigDict, model_validator

from src.constants import LABEL_CLASS_TO_NAME, SentimentLabel


class SimpleModelRequest(BaseModel):
    review: str


class SimpleModelResults(BaseModel):
    NEGATIVE: float
    NEUTRAL: float
    POSITIVE: float

    @model_validator(mode="before")
    @classmethod
    def process_labels(cls, data: dict[int, float]) -> dict[str, float]:
        return {LABEL_CLASS_TO_NAME[key]: value for key, value in data.items()}


class SimpleModelRespone(BaseModel):
    label: SentimentLabel
    score: float

    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="before")
    @classmethod
    def find_highest_score(cls, data: dict[str, float]) -> dict[str, float]:
        highest_label, highest_score = max(
            data.items(),
            key=lambda item: item[1],
        )
        return {"label": highest_label, "score": highest_score}
