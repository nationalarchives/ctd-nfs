import re
import pytest

from src._config.custom_exceptions import FileNamePatternError
from src.pre_instantiation_checker import \
	validate_farm_reference_values, \
	check_values_between_filenames, \
	report_cover_image_inconsistencies, \
	check_document_is_form_and_row_contains_farm_details
from src._config.constants import REGEX	


def setup(test_data, row_num) -> tuple:
	pattern_matches: dict[re.Match] = {
		'filename_1': REGEX.FORM_PATTERN.match(test_data['filename_1']),
		'filename_2': REGEX.FORM_PATTERN.match(test_data['filename_2']),
		'cover': REGEX.COVER_PATTERN.match(test_data['filename_1']),
	}
	row_prefix = f"Row {row_num}"

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
	warning_message = values_between_filenames_different_pieces['warning']
	
	pattern_matches, row_prefix = setup(data, row_num)
	warnings = {'Filename Warnings': [warning_message]}

	assert warnings == check_values_between_filenames(data, pattern_matches, warnings, row_prefix)
