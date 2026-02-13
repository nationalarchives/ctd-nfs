from src.row_data_validator import has_valid_reference_values
from tests.unit.conftest import setup


def test_reference_values_bad_form(reference_values_bad_form):
	pattern_matches, row_prefix = setup(
		reference_values_bad_form['data'],
		reference_values_bad_form['row_num']
		)

	assert not has_valid_reference_values(reference_values_bad_form['data'], pattern_matches, row_prefix)


def test_reference_values_filename1_bad_pattern(reference_values_filename1_bad_pattern):
	pattern_matches, row_prefix = setup(
		reference_values_filename1_bad_pattern['data'],
		reference_values_filename1_bad_pattern['row_num']
		)

	assert not has_valid_reference_values(reference_values_filename1_bad_pattern['data'], pattern_matches, row_prefix)


def test_reference_values_filename2_bad_pattern(reference_values_filename2_bad_pattern):
	pattern_matches, row_prefix = setup(
		reference_values_filename2_bad_pattern['data'],
		reference_values_filename2_bad_pattern['row_num']
		)

	assert not has_valid_reference_values(reference_values_filename2_bad_pattern['data'], pattern_matches, row_prefix)


def test_reference_values_no_farm_data(reference_values_no_farm_data):
	pattern_matches, row_prefix = setup(
		reference_values_no_farm_data['data'],
		reference_values_no_farm_data['row_num']
		)

	assert not has_valid_reference_values(reference_values_no_farm_data['data'], pattern_matches, row_prefix)