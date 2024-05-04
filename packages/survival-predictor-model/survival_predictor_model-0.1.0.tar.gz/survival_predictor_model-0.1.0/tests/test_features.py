from model.config.core import config
from model.processing.features import ExtractLetterTransformer


def test_temporal_variable_transformer(sample_input_data):
    # Given
    transformer = ExtractLetterTransformer(
        variables=config.model_config.vars_to_extract_letter,  # cabin
    )
    assert sample_input_data["cabin"].iat[3] == "E33"

    # When
    subject = transformer.fit_transform(sample_input_data)

    # Then
    assert subject["cabin"].iat[3] == "E"
