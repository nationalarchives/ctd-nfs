from _dataclasses.transcription_checker import TranscriptionChecker


def test_valid_dates(valid_dates):
	for test_date in valid_dates:
		expected_result = None
		actual_result = TranscriptionChecker._vali_dates(test_date)

		assert expected_result == actual_result


def test_dates_with_invalid_format(dates_with_invalid_format):
	for test_date in dates_with_invalid_format['data']:
		expected_message = f"[ERROR] '{test_date}'{dates_with_invalid_format['message']}"
		actual_message = TranscriptionChecker._vali_dates(test_date)

		assert expected_message == actual_message


def test_dates_outside_survey_range(dates_outside_survey_range):
	for test_date in dates_outside_survey_range['data']:
		expected_message = f"[ERROR] '{test_date}'{dates_outside_survey_range['message']}"
		actual_message = TranscriptionChecker._vali_dates(test_date)

		assert expected_message == actual_message


def test_invalid_calendar_dates(invalid_calendar_dates):
	for test_date in invalid_calendar_dates['data']:
		expected_message = f"[ERROR] '{test_date}'{invalid_calendar_dates['message']}"
		actual_message = TranscriptionChecker._vali_dates(test_date)

		assert expected_message == actual_message