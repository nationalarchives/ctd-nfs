import re
import pytest

from src._config.custom_exceptions import FileNamePatternError
from src.pre_instantiation_checker import \
	validate_farm_reference_values, \
	check_values_between_filenames, \
	report_cover_image_inconsistencies, \
	check_document_is_form_and_row_contains_farm_details
from src._config.constants import REGEX	


def setup(test_data) -> tuple:
	pattern_matches: dict[re.Match] = {
		'filename_1': REGEX.FORM_PATTERN.match(test_data['filename_1']),
		'filename_2': REGEX.FORM_PATTERN.match(test_data['filename_2']),
		'cover': REGEX.COVER_PATTERN.match(test_data['filename_1']),
	}
	row_prefix = f"Row {test_data['row_num']}"

	return pattern_matches, row_prefix


def test_farm_reference_values_bad_form(farm_reference_values_bad_form):
	farm_data_row = farm_reference_values_bad_form['data']
	pattern_matches, row_prefix = setup(farm_data_row)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_bad_form['error']):
		validate_farm_reference_values(farm_data_row, pattern_matches, row_prefix)


def test_farm_reference_values_filename1_bad_pattern(farm_reference_values_filename1_bad_pattern):
	farm_data_row = farm_reference_values_filename1_bad_pattern['data']
	pattern_matches, row_prefix = setup(farm_data_row)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_filename1_bad_pattern['error']):
		validate_farm_reference_values(farm_data_row, pattern_matches, row_prefix)


def test_farm_reference_values_filename2_bad_pattern(farm_reference_values_filename2_bad_pattern):
	farm_data_row = farm_reference_values_filename2_bad_pattern['data']
	pattern_matches, row_prefix = setup(farm_data_row)

	with pytest.raises(FileNamePatternError, match=farm_reference_values_filename2_bad_pattern['error']):
		validate_farm_reference_values(farm_data_row, pattern_matches, row_prefix)


# def test_farm_reference_values_no_farm_data(farm_reference_values_no_farm_data):
# 	for test in farm_reference_values_no_farm_data:
# 		_, warnings = check_document_is_form_and_row_contains_farm_details(test['data'])
# 		assert test['warning'] == warnings['Type Warnings'][0]
