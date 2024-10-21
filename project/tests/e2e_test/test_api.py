import pytest
import requests

from src.constants import SentimentLabel
from src.data_models import SimpleModelRequest


@pytest.mark.parametrize(
    "review",
    [
        "This product is amazing!",
        "I'm not sure about this one.",
        "Terrible experience, would not recommend.",
    ],
)
def test_predict_endpoint_with_different_reviews(predict_url, review):
    body = SimpleModelRequest(review=review).model_dump()
    response = requests.post(predict_url, json=body)
    response_json = response.json()
    print(response_json)

    assert response.status_code == 200
    assert response_json["label"] in [label.value for label in SentimentLabel]
    assert 0 <= response_json["score"] <= 1