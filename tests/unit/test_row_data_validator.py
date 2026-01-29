from src.row_data_validator import \
	check_values_between_filenames, \
	vali_dates
from tests.unit.conftest import setup


def test_values_between_filenames_different_pieces(values_between_filenames_different_pieces):
	data = values_between_filenames_different_pieces['data']
	row_num = values_between_filenames_different_pieces['row_num']
	expected_message = values_between_filenames_different_pieces['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {'Filename Warnings': []}
	actual_warnings = check_values_between_filenames(data, pattern_matches, warnings_map, row_prefix)

	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_values_between_filenames_different_parish_numbers(values_between_filenames_different_parish_numbers):
	data = values_between_filenames_different_parish_numbers['data']
	row_num = values_between_filenames_different_parish_numbers['row_num']
	expected_message = values_between_filenames_different_parish_numbers['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {'Filename Warnings': []}
	actual_warnings = check_values_between_filenames(data, pattern_matches, warnings_map, row_prefix)

	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_values_between_filenames_image_number_error(values_between_filenames_image_number_error):
	data = values_between_filenames_image_number_error['data']
	row_num = values_between_filenames_image_number_error['row_num']
	expected_message = values_between_filenames_image_number_error['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {'Filename Warnings': []}
	actual_warnings = check_values_between_filenames(data, pattern_matches, warnings_map, row_prefix)

	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_values_between_filenames_parish_number_mismatch(values_between_filenames_parish_number_mismatch):
	data = values_between_filenames_parish_number_mismatch['data']
	row_num = values_between_filenames_parish_number_mismatch['row_num']
	expected_message = values_between_filenames_parish_number_mismatch['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {'Filename Warnings': []}
	actual_warnings = check_values_between_filenames(data, pattern_matches, warnings_map, row_prefix)

	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_valid_dates(valid_dates):
	for test_date in valid_dates['data']:
		expected_result = None	
		actual_result = vali_dates(test_date)

		assert expected_result == actual_result


def test_dates_with_invalid_format(dates_with_invalid_format):
	for test_date in dates_with_invalid_format['data']:
		expected_message = f"[ERROR] '{test_date}'{dates_with_invalid_format['message']}"
		actual_message = vali_dates(test_date)

		assert expected_message == actual_message


def test_dates_outside_survey_range(dates_outside_survey_range):
	for test_date in dates_outside_survey_range['data']:
		expected_message = f"[ERROR] '{test_date}'{dates_outside_survey_range['message']}"
		actual_message = vali_dates(test_date)

		assert expected_message == actual_message


def test_invalid_calendar_dates(invalid_calendar_dates):
	for test_date in invalid_calendar_dates['data']:
		expected_message = f"[ERROR] '{test_date}'{invalid_calendar_dates['message']}"
		actual_message = vali_dates(test_date)

		assert expected_message == actual_message

