import pytest

from src._dataclasses.transcription_model import Transcription, _normalize_date
from src._tools.helpers import TranscriptionDataError


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
	

# @pytest.mark.skip()
def test_cover_page_with_transcription_values():
    fixture = {
            "filename_1": "MAF32194-1.tif",
            'filename_2': "",
            "document_type": "Cover",
            "county": "WD Westmorland",
            "parish": "1 Ambleside",
            "primary_farm_number": "18",
            "additional_farms": "Outhouse, No 1",
            "farm_name": "The Grove Farm",
            "addressee_title": "[not specified]",
            "addressee_individual_name": "[not specified]",
            "addressee_group_names": "[not specified]",
            "address": "[not specified]",
            "owner_title": "Rev",
            "owner_individual_name": "H R Fleming",
            "owner_group_names": "[not specified]",
            "owner_address": "Rayrigg Hall, Windermere, Westmorland",
            "farmer_title": "[not specified]",
            "farmer_individual_name": "R Nicholson",
            "farmer_group_names": "[not specified]",
            "farmer_address": "The Grove Farm, Ambleside",
            "acreage": "162.5/886.5/1049",
            "OS_map_sheet": "26 NE",
            "field_info_date": "06-Feb-42",
            "primary_record_date": "12-Feb-43",
        }
    
    with pytest.raises(TranscriptionDataError,
					#    match="Form type is 'Cover' but row contains farm details."
					   ):
        Transcription(**fixture)

    
