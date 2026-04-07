from src._dataclasses.transcription_model import _normalize_date


def test_normalize_date(valid_dates, normalized_dates):
	for index, test_date in enumerate(valid_dates):
		expected_result = normalized_dates[index]

		assert expected_result == _normalize_date(test_date)