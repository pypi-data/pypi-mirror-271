import numpy as np

from unsupervised_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_first_predicted_label = 2
    expected_no_predictions = 167
    reduced_pca_shape = (167, 2)

    # When
    results = make_prediction(input_data=sample_input_data)

    # Then
    predictions = results.get("predicted_labels")
    processed_data = results.get("processed_data")
    assert predictions[0] == expected_first_predicted_label
    assert len(predictions) == expected_no_predictions
    assert processed_data.shape == reduced_pca_shape
    assert any(np.unique(predictions) == np.array([0, 1, 2, 3]))
