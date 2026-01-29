from src._config.custom_exceptions import FileNamePatternError
from src.row_data_validator import validate_farm_reference_values
from tests.unit.conftest import setup


import pytest


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