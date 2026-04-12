import pytest


@pytest.fixture()
def base_farm():
	return {
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

