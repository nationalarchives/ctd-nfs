from src._dataclasses.transcription_model import Transcription
from src._dataclasses.transcription_checker import TranscriptionChecker


fixture = {
	'primary_farm_number': "18",
	'additional_farms': "Outhouse, No 1",
	'farm_name': "The Grove Farm",
	'addressee_title': "[not specified]",
	'addressee_individual_name': "[not specified]",
	'addressee_group_names': "[not specified]",
	'address': "[not specified]",
	'owner_title': "Rev",
	'owner_individual_name': "H R Fleming",
	'owner_group_names': "[not specified]",
	'owner_address': "Rayrigg Hall, Windermere, Westmorland",
	'farmer_title': "[not specified]",
	'farmer_individual_name': "R Nicholson",
	'farmer_group_names': "[not specified]",
	'farmer_address': "The Grove Farm, Ambleside",
	'acreage': "162.5/886.5/1049",
	'OS_map_sheet': "26 NE",
	'field_info_date': "06-Feb-42",
	'primary_record_date': "12-Feb-43",
}


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