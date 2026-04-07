from src._dataclasses.transcription_model import Transcription, _normalize_date


def test_normalize_date(valid_dates, normalized_dates):
	for index, test_date in enumerate(valid_dates):
		expected_result = normalized_dates[index]

		assert expected_result == _normalize_date(test_date)


def test_reference_values_no_farm_data():
	fixture = {
        'filename_1': "MAF32-194-1_59.tif",
        'filename_2': "MAF32-194-1_60.tif",
        'document_type': "B496/EI",
        'county': "WD Westmorland",
        'parish': "1 Ambleside",
        'primary_farm_number': "[not specified]",
        'additional_farms': "[not specified]",
        'farm_name': "[not specified]",
        'addressee_title': "[not specified]",
        'addressee_individual_name': "[not specified]",
        'addressee_group_names': "[not specified]",
        'address': "[not specified]",
        'owner_title': "[not specified]",
        'owner_individual_name': "[not specified]",
        'owner_group_names': "[not specified]",
        'owner_address': "[not specified]",
        'farmer_title': "[not specified]",
        'farmer_individual_name': "[not specified]",
        'farmer_group_names': "[not specified]",
        'farmer_address': "[not specified]",
        'acreage': "[not specified]",
        'OS_map_sheet': "[not specified]",
        'field_info_date': "[not specified]",
        'primary_record_date': "[not specified]",
    }
	test = Transcription(**fixture)
	assert test.no_data
	
