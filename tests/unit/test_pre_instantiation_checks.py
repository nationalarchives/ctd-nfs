import re
import pytest

from src._config.custom_exceptions import FileNamePatternError
from row_data_validator import \
	validate_farm_reference_values, \
	check_values_between_filenames, \
	report_cover_image_inconsistencies, \
	check_for_cover_with_farm_details, \
	date_check
from src._config.constants import REGEX


def setup(test_data, row_num) -> tuple:
	pattern_matches: dict[re.Match] = {
		'filename_1': REGEX.FORM_PATTERN.match(test_data['filename_1']),
		'filename_2': REGEX.FORM_PATTERN.match(test_data['filename_2']),
		'cover': REGEX.COVER_PATTERN.match(test_data['filename_1']),
	}
	row_prefix = f"Row {row_num}: "

	return pattern_matches, row_prefix

def test_farm_reference_values_bad_form(farm_reference_values_bad_form):
	pattern_matches, row_prefix = setup(
		farm_reference_values_bad_form['data'],
		farm_reference_values_bad_form['row_num']
		)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_bad_form['error']):
		validate_farm_reference_values(farm_reference_values_bad_form['data'], pattern_matches, row_prefix)


def test_farm_reference_values_filename1_bad_pattern(farm_reference_values_filename1_bad_pattern):
	pattern_matches, row_prefix = setup(
		farm_reference_values_filename1_bad_pattern['data'],
		farm_reference_values_filename1_bad_pattern['row_num']
		)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_filename1_bad_pattern['error']):
		validate_farm_reference_values(farm_reference_values_filename1_bad_pattern['data'], pattern_matches, row_prefix)


def test_farm_reference_values_filename2_bad_pattern(farm_reference_values_filename2_bad_pattern):
	pattern_matches, row_prefix = setup(
		farm_reference_values_filename2_bad_pattern['data'],
		farm_reference_values_filename2_bad_pattern['row_num']
		)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_filename2_bad_pattern['error']):
		validate_farm_reference_values(farm_reference_values_filename2_bad_pattern['data'], pattern_matches, row_prefix)


def test_farm_reference_values_no_farm_data(farm_reference_values_no_farm_data):
	pattern_matches, row_prefix = setup(
		farm_reference_values_no_farm_data['data'],
		farm_reference_values_no_farm_data['row_num']
		)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_no_farm_data['error']):
		validate_farm_reference_values(farm_reference_values_no_farm_data['data'], pattern_matches, row_prefix)


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


def test_cover_image_inconsistencies_bad_cover_pattern(cover_image_inconsistencies_bad_cover_pattern):
	data = cover_image_inconsistencies_bad_cover_pattern['data']
	row_num = cover_image_inconsistencies_bad_cover_pattern['row_num']
	expected_message = cover_image_inconsistencies_bad_cover_pattern['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {
		'Filename Warnings': [],
		'Type Warnings': []
		}

	actual_warnings = report_cover_image_inconsistencies(data, pattern_matches, warnings_map, row_prefix)
	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_cover_with_two_images_1(cover_image_inconsistencies_cover_with_two_images_1):
	data = cover_image_inconsistencies_cover_with_two_images_1['data']
	row_num = cover_image_inconsistencies_cover_with_two_images_1['row_num']
	expected_message = cover_image_inconsistencies_cover_with_two_images_1['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {
		'Filename Warnings': [],
		'Type Warnings': []
		}
	actual_warnings = report_cover_image_inconsistencies(data, pattern_matches, warnings_map, row_prefix)
	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_cover_with_two_images_2(cover_image_inconsistencies_cover_with_two_images_2):
	data = cover_image_inconsistencies_cover_with_two_images_2['data']
	row_num = cover_image_inconsistencies_cover_with_two_images_2['row_num']
	expected_message = cover_image_inconsistencies_cover_with_two_images_2['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {
		'Filename Warnings': [],
		'Type Warnings': []
		}
	actual_warnings = report_cover_image_inconsistencies(data, pattern_matches, warnings_map, row_prefix)
	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_form_supplied_but_cover_image(cover_image_inconsistencies_form_supplied_but_cover_image):
	data = cover_image_inconsistencies_form_supplied_but_cover_image['data']
	row_num = cover_image_inconsistencies_form_supplied_but_cover_image['row_num']
	expected_message = cover_image_inconsistencies_form_supplied_but_cover_image['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {
		'Filename Warnings': [],
		'Type Warnings': []
		}
	actual_warnings = report_cover_image_inconsistencies(data, pattern_matches, warnings_map, row_prefix)
	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_form_supplied_but_cover_pattern(cover_image_inconsistencies_form_supplied_but_cover_pattern):
	data = cover_image_inconsistencies_form_supplied_but_cover_pattern['data']
	row_num = cover_image_inconsistencies_form_supplied_but_cover_pattern['row_num']
	expected_message = cover_image_inconsistencies_form_supplied_but_cover_pattern['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings_map = {
		'Filename Warnings': [],
		'Type Warnings': []
		}
	actual_warnings = report_cover_image_inconsistencies(data, pattern_matches, warnings_map, row_prefix)
	assert expected_message == actual_warnings['Filename Warnings'][0]


def test_cover_with_farm_details(cover_with_farm_details):
	for test_data in cover_with_farm_details:
		data = test_data['data']
		row_num = test_data['row_num']
		expected_message = test_data['warning']
		
		pattern_matches, row_prefix = setup(data, row_num)
		warnings_map = {
			'Filename Warnings': [],
			'Type Warnings': []
			}
		actual_warnings = check_for_cover_with_farm_details(data, pattern_matches, warnings_map, row_prefix)
		assert expected_message == actual_warnings['Filename Warnings'][0]


def test_valid_dates(valid_dates):
	for test_date in valid_dates['data']:
		expected_result = None	
		actual_result = date_check(test_date)

		assert expected_result == actual_result


def test_dates_with_invalid_format(dates_with_invalid_format):
	for test_date in dates_with_invalid_format['data']:
		expected_message = f"[ERROR] '{test_date}'{dates_with_invalid_format['message']}"
		actual_message = date_check(test_date)

		assert expected_message == actual_message


def test_dates_outside_survey_range(dates_outside_survey_range):
	for test_date in dates_outside_survey_range['data']:
		expected_message = f"[ERROR] '{test_date}'{dates_outside_survey_range['message']}"
		actual_message = date_check(test_date)

		assert expected_message == actual_message


def test_invalid_calendar_dates(invalid_calendar_dates):
	for test_date in invalid_calendar_dates['data']:
		expected_message = f"[ERROR] '{test_date}'{invalid_calendar_dates['message']}"
		actual_message = date_check(test_date)

		assert expected_message == actual_message
	