from src.harvester.transcription_checker import TranscriptionChecker


def test_valid_dates():
	fixture = [
		"15 October 1941",
		"January 1942",
		"4 July 1942",
		"05 July 1942",
		"July 1941",
		"1943",
		"01/05/1942",
		"6-6-1942",
		"12.12.1943",
		"1/1/42",
		"6 Jun",
		"03 February",
		"Sep",
		"November",
	]
	for test_date in fixture:
		expected_result = None
		actual_result = TranscriptionChecker._vali_dates(test_date)

		assert expected_result == actual_result


def test_dates_with_invalid_format():
	fixture = [
		"10 1942",
		"4th July 1942",
		"5th 1943",
	]
	for test_date in fixture:
		expected_message = f"[ERROR] '{test_date}' is not a valid format. Further date checks cannot be performed."
		actual_message = TranscriptionChecker._vali_dates(test_date)

		assert expected_message == actual_message


def test_dates_outside_survey_range():
	fixture = [
		"September 1945",
		"31 October 1940",
	]
	for test_date in fixture:
		expected_message = f"[ERROR] '{test_date}' is outside the survey timespan."
		actual_message = TranscriptionChecker._vali_dates(test_date)

		assert expected_message == actual_message


def test_invalid_calendar_dates():
	fixture = [
		"32 March 1942",
		"29 February 1943",
		"30 February",
	]
	for test_date in fixture:
		expected_message = f"[ERROR] '{test_date}' is not a valid calendar date."
		actual_message = TranscriptionChecker._vali_dates(test_date)

		assert expected_message == actual_message

