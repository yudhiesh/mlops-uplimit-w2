import pytest
from src.model import Model
from src.data_models import SimpleModelResponse
from src.constants import LABEL_CLASS_TO_NAME

@pytest.fixture(scope="module")
def session():
    return Model.load_model()

def get_sentiment(session, text: str) -> str:
    label_scores = Model.predict(session, text)
    label_scores_mapped = {LABEL_CLASS_TO_NAME[k]: v for k, v in label_scores.items()}
    print(f"Mapped label scores: {label_scores_mapped}")
    response = SimpleModelResponse.model_validate(label_scores_mapped)

    # Return the predicted label
    return response.label

@pytest.mark.parametrize(
    "input_a, input_b, expected_label",
    [
        (
            "I absolutely love this product! It has changed my life.",
            "This product is amazing! It has been a life-changer for me.",
            "POSITIVE",
        ),
        (
            "I hate this item. It doesn't work at all.",
            "This is the worst product ever. Completely non-functional.",
            "NEGATIVE",
        ),
    ],
)
def test_invariance(input_a, input_b, expected_label, session):
    """INVariance tests: inputs with similar meaning should yield the same sentiment."""
    label_a = get_sentiment(session, input_a)
    label_b = get_sentiment(session, input_b)
    assert label_a == label_b == expected_label

@pytest.mark.parametrize(
    "input_before, input_after, expected_label_before, expected_label_after",
    [
        (
            "I like this product.",
            "I don't like this product.",
            "POSITIVE",
            "NEGATIVE",
        ),
        (
            "The service was good.",
            "The service was extremely good.",
            "POSITIVE",
            "POSITIVE",
        ),
    ],
)
def test_directional(input_before, input_after, expected_label_before, expected_label_after, session):
    """DIRectional tests: changes in input should cause expected changes in sentiment."""
    label_before = get_sentiment(session, input_before)
    label_after = get_sentiment(session, input_after)
    assert label_before == expected_label_before
    assert label_after == expected_label_after

@pytest.mark.parametrize(
    "input_text, expected_label",
    [
        ("This is the best purchase I've ever made!", "POSITIVE"),
        ("Absolutely terrible experience. Will not buy again.", "NEGATIVE"),
    ],
)
def test_mft(input_text, expected_label, session):
    """Minimum Functionality Tests: simple inputs with expected sentiments."""
    prediction = get_sentiment(session, input_text)
    assert prediction == expected_label