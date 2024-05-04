import numpy as np

from sklearn.metrics import accuracy_score
from model.predict import make_prediction


def test_prediction_against_truth_value(sample_input_data):
    # When
    estimated_results = make_prediction(input_data=sample_input_data)

    # Then
    predictions = estimated_results.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.int64)
    assert estimated_results.get("errors") is None
    _predictions = list(predictions)
    y_true = sample_input_data["survived"]
    accuracy = accuracy_score(y_true, _predictions)
    assert accuracy > 0.7
