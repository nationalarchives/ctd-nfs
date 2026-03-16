from src.harvester.row_data_validator import check_for_cover_with_farm_details, report_cover_image_inconsistencies
from tests.unit.conftest import setup


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