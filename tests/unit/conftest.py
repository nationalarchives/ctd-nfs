import pytest
import re

from src._config.constants import REGEX
from src.harvester.farm_setup import Form, initialise_forms_mapping


def setup(test_data, row_num) -> tuple:
	pattern_matches: dict[re.Match] = {
		'filename_1': REGEX.FORM_PATTERN.match(test_data['filename_1']),
		'filename_2': REGEX.FORM_PATTERN.match(test_data['filename_2']) if test_data['filename_2'] else REGEX.FORM_PATTERN.match(""),
		'cover': REGEX.COVER_PATTERN.match(test_data['filename_1']),
	}
	row_prefix = f"Row {row_num}: "

	return pattern_matches, row_prefix


@pytest.fixture()
def farms():
    return [
		{
			"filename_1": "MAF32-194-1_59.tif",
			"filename_2": "MAF32-194-1_60.tif",
			"document_type": "B496/EI",
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
		},
		{
			"filename_1": "MAF32-194-1_75.tif",
			"filename_2": "MAF32-194-1_76.tif",
			"document_type": "C 47/SSY",
			"county": "WD Westmorland",
			"parish": "1 Ambleside",
			"primary_farm_number": "19",
			"additional_farms": "[not specified]",
			"farm_name": "[not specified]",
			"addressee_title": "Mr",
			"addressee_individual_name": "W Parsons",
			"addressee_group_names": "[not specified]",
			"address": "Gale House, Ambleside, Westmorland",
			"owner_title": "[not specified]",
			"owner_individual_name": "[not specified]",
			"owner_group_names": "R T E Conant, Agents Smith and Co; The Crown, Carter Jonas and Sons; Rev Barston",
			"owner_address": "[not specified]",
			"farmer_title": "[not specified]",
			"farmer_individual_name": "[not specified]",
			"farmer_group_names": "[not specified]",
			"farmer_address": "[not specified]",
			"acreage": "[not specified]",
			"OS_map_sheet": "[not specified]",
			"field_info_date": "[not specified]",
			"primary_record_date": "[not specified]",
		},
		{
			"filename_1": "MAF32-228-1_23.tif",
			"filename_2": "MAF32-228-1_24.tif",
			"document_type": "B496/EI",
			"county": "DM Durham",
			"parish": "1 Barnard Castle",
			"primary_farm_number": "4",
			"additional_farms": "[not specified]",
			"farm_name": "9 King Street",
			"addressee_title": "[not specified]",
			"addressee_individual_name": "[not specified]",
			"addressee_group_names": "[not specified]",
			"address": "[not specified]",
			"owner_title": "[not specified]",
			"owner_individual_name": "[not specified]",
			"owner_group_names": "Mr Kellett; Mr Swift; Mr W Bain; Mrs Mane; Mrs Todd; W Walton",
			"owner_address": "8 Sendal, Yorkshire; Barnard Castle; Darlington Road, Barnard Castle; Gallowgate, Barnard Castle; Gallowgate, Barnard Castle; 24 Coronation Road, Redcar",
			"farmer_title": "[not specified]",
			"farmer_individual_name": "W J Chaplow",
			"farmer_group_names": "[not specified]",
			"farmer_address": "Barnard Castle",
			"acreage": "30/Nil Acres",
			"OS_map_sheet": "XL NE 1898",
			"field_info_date": "[not specified]",
			"primary_record_date": "19 April 1943",
		},
		{
			"filename_1": "MAF32-247-23_75.tif",
			"filename_2": "MAF32-247-23_76.tif",
			"document_type": "B496/EI",
			"county": "RD Rutland",
			"parish": "23 Hambleton",
			"primary_farm_number": "19",
			"additional_farms": "[not specified]",
			"farm_name": "Armley Lodge",
			"addressee_title": "[not specified]",
			"addressee_individual_name": "[not specified]",
			"addressee_group_names": "[not specified]",
			"address": "[not specified]",
			"owner_title": "[not specified]",
			"owner_individual_name": "[not specified]",
			"owner_group_names": "Nichols, Agent for the Earl of Ancaster",
			"owner_address": "Hambleton, Oakham",
			"farmer_title": "[not specified]",
			"farmer_individual_name": "[not specified]",
			"farmer_group_names": "Woodhead Bros",
			"farmer_address": "Hambleton, Oakham",
			"acreage": "Arable 127.5; Grass 45; 172.5",
			"OS_map_sheet": "9 NE1931 Edition",
			"field_info_date": "30 January 1942",
			"primary_record_date": "[not specified]"
		}
	]


@pytest.fixture()
def concatenation_data():
	return {
		'10 Burley/7': {
			'data': [
				{
					'filename_1': "MAF32-346-10_9.tif",
					'filename_2': "MAF32-346-10_10.tif",
					'document_type': "C51/SSY",
					'county': "RD Rutland",
					'parish': "10 Burley",
					'primary_farm_number': "7",
					'additional_farms': "[not specified]",
					'farm_name': "Glebe Farm",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "A Lane and C Lane",
					'address': "Burley, Oakham, Rutland",
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
				},
				{
					'filename_1': "MAF32-346-10_27.tif",
					'filename_2': "MAF32-346-10_28.tif",
					'document_type': "B496/EI",
					'county': "RD Rutland",
					'parish': "10 Burley",
					'primary_farm_number': "7",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "[not specified]",
					'address': "[not specified]",
					'owner_title': "[not specified]",
					'owner_individual_name': "[not specified]",
					'owner_group_names': "Burley Estate",
					'owner_address': "[not specified]",
					'farmer_title': "[not specified]",
					'farmer_individual_name': "[not specified]",
					'farmer_group_names': "A Lane and C Lane",
					'farmer_address': "Burley, Oakham, Rutland",
					'acreage': "168 ac",
					'OS_map_sheet': "V 15",
					'field_info_date': "September 1942",
					'primary_record_date': "[not specified]",
				},
			],
			'result': {
				'farm_name': ["Glebe Farm", "[not specified]"],
			},
		},
		'49 Tickencote/6': {
			'data': [
				{
					'filename_1': "MAF32-348-49_23.tif",
					'filename_2': "MAF32-348-49_24.tif",
					'document_type': "C 47/SSY",
					'county': "RD Rutland",
					'parish': "49 Tickencote",
					'primary_farm_number': "6",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "Rutland WAEC",
					'address': "Lodge Farm, Tickencote, Stamford, Lincolnshire",
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
				},
				{
					'filename_1': "MAF32-348-49_25.tif",
					'filename_2': "MAF32-348-49_26.tif",
					'document_type': "C 47/SSY",
					'county': "RD Rutland",
					'parish': "49 Tickencote",
					'primary_farm_number': "6",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "The Rutland War Agricultural Committee",
					'address': "Lodge Farm, Tickencote, Stamford, Lincolnshire",
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
				},
			],
			'result': {
				'addressee_group_names': ["Rutland WAEC", "The Rutland War Agricultural Committee"],
			},
		},
		'96 Cockermouth/10': {
			'data': [
				{
					'filename_1': "MAF32-176-100_67.tif",
					'filename_2': "MAF32-176-100_68.tif",
					'document_type': "C51/SSY",
					'county': "CU Cumberland",
					'parish': "96 Cockermouth",
					'primary_farm_number': "10",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "Mr",
					'addressee_individual_name': "W Mitchell",
					'addressee_group_names': "[not specified]",
					'address': "Waste Lane, Cockermouth",
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
				},
				{
					'filename_1': "MAF32-176-100_221.tif",
					'filename_2': "MAF32-176-100_222.tif",
					'document_type': "C 47/SSY",
					'county': "CU Cumberland",
					'parish': "96 Cockermouth",
					'primary_farm_number': "10",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "Mr",
					'addressee_individual_name': "Wm Mitchell",
					'addressee_group_names': "[not specified]",
					'address': "Dairyman, Cockermouth, Cumberland",
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
				},
			],
			'result': {
				'addressee_group_names': ["[not specified]", "[not specified]"],
			},
	 	},
		'97 Dean/47': {
			'data': [
				{
					'filename_1': "MAF32-175-97_89.tif",
					'filename_2': "MAF32-175-97_90.tif",
					'document_type': "C51/SSY",
					'county': "CU Cumberland",
					'parish': "97 Dean",
					'primary_farm_number': "47",
					'additional_farms': "[not specified]",
					'farm_name': "Branthwaite Mill, North Workington",
					'addressee_title': "Mr",
					'addressee_individual_name': "Wm West",
					'addressee_group_names': "[not specified]",
					'address': "Branthwaite Mill, North Workington",
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
				},
				{
					'filename_1': "MAF32-175-97_237.tif",
					'filename_2': "MAF32-175-97_238.tif",
					'document_type': "B496/EI",
					'county': "CU Cumberland",
					'parish': "97 Dean",
					'primary_farm_number': "47",
					'additional_farms': "[not specified]",
					'farm_name': "Branthwaite Mill",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "[not specified]",
					'address': "[not specified]",
					'owner_title': "[not specified]",
					'owner_individual_name': "[not specified]",
					'owner_group_names': "[not specified]",
					'owner_address': "[not specified]",
					'farmer_title': "[not specified]",
					'farmer_individual_name': "Wm West",
					'farmer_group_names': "[not specified]",
					'farmer_address': "Branthwaite Mill, Branthwaite, Workington",
					'acreage': "35/-/35",
					'OS_map_sheet': "XLII 1926",
					'field_info_date': "27 August 1941",
					'primary_record_date': "[not specified]",
				},
			],
			'result': {
				'addressee_title': ["Mr", "[not specified]"],
			},
		},
		'296 Farmborough/14': {
			'data': [
				{
					'filename_1': "MAF32-134-296_45.tif",
					'filename_2': "MAF32-134-296_46.tif",
					'document_type': "C51/SSY",
					'county': "ST Somerset",
					'parish': "296 Farmborough",
					'primary_farm_number': "14",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "Mr",
					'addressee_individual_name': "F Notley",
					'addressee_group_names': "[not specified]",
					'address': "Hillside Farm, Farmborough, Bath",
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
				},
				{
					'filename_1': "MAF32-134-296_53.tif",
					'filename_2': "MAF32-134-296_54.tif",
					'document_type': "B496/EI",
					'county': "ST Somerset",
					'parish': "296 Farmborough",
					'primary_farm_number': "14",
					'additional_farms': "[not specified]",
					'farm_name': "Hillside Farm",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "[not specified]",
					'address': "[not specified]",
					'owner_title': "[not specified]",
					'owner_individual_name': "[not specified]",
					'owner_group_names': ["F A C Notley", "Mrs Bridges"],
					'owner_address': ["Bloomfield, Timsbury", "Timsbury, Near Bath"],
					'farmer_title': "[not specified]",
					'farmer_individual_name': "L Gregory",
					'farmer_group_names': "[not specified]",
					'farmer_address': "Hillside Farm, Farmborough, Near Bath",
					'acreage': "50",
					'OS_map_sheet': "XIII SW 2nd Edition 1903",
					'field_info_date': "26/02/1944",
					'primary_record_date': "23/05/1944",
				},
			],
			'result': {
				'farm_name': ["[not specified]", "Hillside Farm"],
			},
		},
		'91 Dulverton/26': {
			'data': [
				{
					'filename_1': "MAF32-131-91_41.tif",
					'filename_2': "MAF32-131-91_42.tif",
					'document_type': "C51/SSY",
					'county': "ST Somerset",
					'parish': "91 Dulverton",
					'primary_farm_number': "26",
					'additional_farms': "[not specified]",
					'farm_name': "Beasley Farm",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "E I Kemp",
					'addressee_group_names': "[not specified]",
					'address': "High Street, Dulverton",
					'owner_title': "[not specified]",
					'owner_individual_name': "[not specified]",
					'owner_group_names': "[not specified]",
					'owner_address': ["Dulverton, West Somerset", "The Cottage, Dulverton, Somerset", "Green Hotel, Dulverton"],
					'farmer_title': "[not specified]",
					'farmer_individual_name': "[not specified]",
					'farmer_group_names': "[not specified]",
					'farmer_address': "[not specified]",
					'acreage': "[not specified]",
					'OS_map_sheet': "[not specified]",
					'field_info_date': "[not specified]",
					'primary_record_date': "[not specified]",
				},
				{
					'filename_1': "MAF32-131-91_137.tif",
					'filename_2': "MAF32-131-91_138.tif",
					'document_type': "B496/EI",
					'county': "ST Somerset",
					'parish': "91 Dulverton",
					'primary_farm_number': "26",
					'additional_farms': "[not specified]",
					'farm_name': "High Street",
					'addressee_title': "[not specified]",
					'addressee_individual_name': "[not specified]",
					'addressee_group_names': "[not specified]",
					'address': "[not specified]",
					'owner_title': "[not specified]",
					'owner_individual_name': "[not specified]",
					'owner_group_names':["The Hon Mrs Herbert Pixton", "Hon Mrs Pixton", "Mr Abbott", "Mrs Surridge", "Miss Dowey"],
					'owner_address': ["Dulverton", "Dulverton", "The Cottage, Dulverton", "Exter", "Green Hotel, Dulverton"],
					'farmer_title': "[not specified]",
					'farmer_individual_name': "[not specified]",
					'farmer_group_names': "E S Kemp and Sons",
					'farmer_address': "High Street and Beasly Farm, Dulverton",
					'acreage': "[not specified]",
					'OS_map_sheet': "LXVII NW 2nd Edition 1905",
					'field_info_date': "[not specified]",
					'primary_record_date': "02/01/1944",
				},
			],
			'result': {
                'owner_address': ["Dulverton, West Somerset", "The Cottage, Dulverton, Somerset", "Green Hotel, Dulverton", "Dulverton", "Dulverton", "The Cottage, Dulverton", "Exter", "Green Hotel, Dulverton"],
			},
		},
		'1 Ashwell/4': {
			'data': [
				{
					'filename_1': "MAF32-346-1_7.tif",
					'filename_2': "MAF32-346-1_8.tif",
					'document_type': "C51/SSY",
					'county': "RD Rutland",
					'parish': "1 Ashwell",
					'primary_farm_number': "4",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "Capt Hon",
					'addressee_individual_name': "L E Lowther",
					'addressee_group_names': "[not specified]",
					'address': "Ashwell Hill, Ashwell, Oakham, Rutland",
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
					'primary_record_date': "[not specified]"
				},
				{
					'filename_1': "MAF32-346-1_89.tif",
					'filename_2': "MAF32-346-1_90.tif",
					'document_type': "C 47/SSY",
					'county': "RD Rutland",
					'parish': "1 Ashwell",
					'primary_farm_number': "4",
					'additional_farms': "[not specified]",
					'farm_name': "[not specified]",
					'addressee_title': "Capt Hon",
					'addressee_individual_name': "L E Lowther",
					'addressee_group_names': "[not specified]",
					'address': "Ashwell Hill, Ashwell, Oakham, Rutland",
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
					'primary_record_date': "[not specified]"
				}
			],
			'result': {
                'address': ["Ashwell Hill, Ashwell, Oakham, Rutland", "Ashwell Hill, Ashwell, Oakham, Rutland"],
			}
		}
	}


@pytest.fixture()
def concatenate_forms_fixture():
	fields = ["filename_1", "filename_2", "document_type", "field_info_date", "primary_record_date",]
	farms = [
		[
			["MAF32-171-115_1.tif", "MAF32-171-115_2.tif", "C51/SSY", "[not specified]", "[not specified]",],
			["MAF32-171-115_89.tif", "MAF32-171-115_90.tif", "B496/EI", "18 August 1941", "[not specified]",],
			["MAF32-171-115_91.tif", "MAF32-171-115_92.tif", "B496/EI", "[not specified]", "[not specified]",],
			["MAF32-171-115_253.tif", "MAF32-171-115_254.tif", "C 47/SSY", "[not specified]", "[not specified]",],
			["MAF32-171-115_343.tif", "MAF32-171-115_344.tif", "SF C69/SSY", "[not specified]", "[not specified]",],
			["MAF32-171-115_345.tif", "MAF32-171-115_346.tif", "SF", "[not specified]", "[not specified]",],
		],
		[
			["MAF32-167-29_1.tif","MAF32-167-29_2.tif", "C51/SSY", "[not specified]", "[not specified]",],
			["MAF32-167-29_23.tif", "MAF32-167-29_24.tif", "B496/EI", "November 1942", "December 1943",],
			["MAF32-167-29_25.tif", None, "B496/EI", "[not specified]", "[not specified]",],
			["MAF32-167-29_56.tif", "MAF32-167-29_57.tif", "C 47/SSY", "[not specified]", "[not specified]",],
			["MAF32-167-29_82.tif", "MAF32-167-29_83.tif", "SF", "[not specified]", "[not specified]",],
		]
	]

	fixture_data = []
	for document_set in farms:
		farm = []
		for form_data in document_set:
			set_of_forms = initialise_forms_mapping()
			item = dict(zip(fields, form_data))
			pics = [item[key]
				for key in ["filename_1", "filename_2"]
				if item[key]
			]
			set_of_forms[item['document_type']].append(Form(images=pics, field_info_date=item['field_info_date'], primary_record_date=item['primary_record_date']))
			farm.append(set_of_forms)

		fixture_data.append(farm)

	return fixture_data


@pytest.fixture()
def bad_farm_initial_values():
	return	[
		{
			'data':{
				'row_num': '6666',
				"filename_1": "MAF32-167-28_386.tif",
				"filename_2": "MAF32-167-28_385.tif",
				"document_type": "C 47/SSY",
				"county": "CU Cumberland",
				"parish": "28 Aikton",
			},
			'warning': "Row 6666: MAF32-167-28_386.tif and MAF32-167-28_385.tif are either not consecutive images or in the wrong order."
		},
	]


@pytest.fixture()
def reference_values_bad_form():
	return	{
			'row_num': "10101",
			'data':{
				"filename_1": "MAF32-51-285.tif",
				'filename_2': None,
				"document_type": "SF47/SSY",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
		}	


@pytest.fixture()
def reference_values_filename1_bad_pattern():
	return	{
			'row_num': "10101",
			'data':{
				"filename_1": "MAF32-51.tif",
				'filename_2': None,
				"document_type": "C 49/SSY",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
		}		


@pytest.fixture()
def reference_values_filename2_bad_pattern():
	return	{
			'row_num': "10101",
			'data':{
				"filename_1": "MAF32-51-285.tif",
				"filename_2": "MAF3251286.tif",
				"document_type": "SF C69/SSY",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
		}	


@pytest.fixture()
def reference_values_no_farm_data():
	return	{
			'row_num': "10101",
			'data':{
				"filename_1": "MAF32-194-1_59.tif",
				"filename_2": "MAF32-194-1_60.tif",
				"document_type": "B496/EI",
				"county": "WD Westmorland",
				"parish": "1 Ambleside",
				"primary_farm_number": "[not specified]",
				"additional_farms": "[not specified]",
				"farm_name": "[not specified]",
				"addressee_title": "[not specified]",
				"addressee_individual_name": "[not specified]",
				"addressee_group_names": "[not specified]",
				"address": "[not specified]",
				"owner_title": "[not specified]",
				"owner_individual_name": "[not specified]",
				"owner_group_names": "[not specified]",
				"owner_address": "[not specified]",
				"farmer_title": "[not specified]",
				"farmer_individual_name": "[not specified]",
				"farmer_group_names": "[not specified]",
				"farmer_address": "[not specified]",
				"acreage": "[not specified]",
				"OS_map_sheet": "[not specified]",
				"field_info_date": "[not specified]",
				"primary_record_date": "[not specified]",
			},
	}		


@pytest.fixture()
def values_between_filenames_different_pieces():
	return	{
		'row_num': "1111",
		'data':{
			"filename_1": "MAF32-194-1_59.tif",
			"filename_2": "MAF32-195-1_60.tif",
			"document_type": "C51/SSY",
			"county": "WD Westmorland",
			"parish": "1 Ambleside",
		},
		'warning': "Row 1111: MAF32-194-1_59.tif and MAF32-195-1_60.tif have different pieces."
	}


@pytest.fixture()
def values_between_filenames_different_parish_numbers():
	return	{
		'row_num': "2222",
		'data':{
			"filename_1": "MAF32-5-98_28.tif",
			"filename_2": "MAF32-5-96_29.tif",
			"document_type": "B496/EI",
			"county": "HF Herefordshire",
			"parish": "98 Clehonger",
		},
		'warning': "Row 2222: MAF32-5-98_28.tif and MAF32-5-96_29.tif have different parish numbers."
	}


@pytest.fixture()
def values_between_filenames_image_number_error():
	return	{
		'row_num': "3333",
		'data':{
			"filename_1": "MAF32-167-28_386.tif",
			"filename_2": "MAF32-167-28_388.tif",
			"document_type": "C 47/SSY",
			"county": "CU Cumberland",
			"parish": "28 Aikton",
		},
		'warning': "Row 3333: MAF32-167-28_386.tif and MAF32-167-28_388.tif are either not consecutive images or in the wrong order."
	}


@pytest.fixture()
def values_between_filenames_parish_number_mismatch():
	return	{
		'row_num': "4444",
		'data':{
			"filename_1": "MAF32-5-96_28.tif",
			"filename_2": "MAF32-5-96_29.tif",
			"document_type": "B496/EI",
			"county": "HF Herefordshire",
			"parish": "98 Clehonger",
		},
		'warning': "Row 4444: MAF32-5-96_28.tif and MAF32-5-96_29.tif have a different parish number from parish name '98 Clehonger'."
	}


@pytest.fixture()
def cover_image_inconsistencies_bad_cover_pattern():
	return {
			'row_num': '5555',
			'data':{
				"filename_1": "MAF32-194-1_59.tif",
				"filename_2": None,
				"document_type": "Cover",
				"county": "WD Westmorland",
				"parish": "1 Ambleside",
			},
			'warning': "Row 5555: Form type is 'Cover' but MAF32-194-1_59.tif does not match expected cover pattern or have image number 0001."
		}


@pytest.fixture()
def cover_image_inconsistencies_cover_with_two_images_1():
	return {
			'row_num': '6666',
			'data':{
				"filename_1": "MAF32-193-203_97.tif",
				"filename_2": "MAF32-193-203_98.tif",
				"document_type": "Cover",
				"county": "CU Cumberland",
				"parish": "203 Winscales",
			},
			'warning': "Row 6666: Form type is 'Cover' but two form images were provided: MAF32-193-203_97.tif and MAF32-193-203_98.tif."
		}


@pytest.fixture()
def cover_image_inconsistencies_cover_with_two_images_2():
	return {
			'row_num': '8888',
			'data':{
				"filename_1": "MAF32-51-285_0001.tif",
				"filename_2": "MAF32-51-285_0002.tif",
				"document_type": "Cover",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 8888: Form type is 'Cover', and MAF32-51-285_0001.tif matches expected pattern for cover image but additional image MAF32-51-285_0002.tif was also provided."
		}


@pytest.fixture()
def cover_image_inconsistencies_form_supplied_but_cover_image():
	return {
			'row_num': '7777',
			'data':{
				"filename_1": "MAF32-51-285_0001.tif",
				'filename_2': None,
				"document_type": "SF",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 7777: MAF32-51-285_0001.tif matches expected cover pattern or has image number 0001 but form type is 'SF'."
		}


@pytest.fixture()
def cover_image_inconsistencies_form_supplied_but_cover_pattern():
	return {
			'row_num': '9999',
			'data':{
				"filename_1": "MAF32-51-285.tif",
				'filename_2': None,
				"document_type": "SF",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 9999: MAF32-51-285.tif matches expected cover pattern or has image number 0001 but form type is 'SF'."
	}


@pytest.fixture()
def cover_with_farm_details():
	return	[
		{
			'row_num': "10101",
			'data':{
				"filename_1": "MAF32-194-1.tif",
				'filename_2': None,
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
			},
			'warning': "Row 10101: Form type is 'Cover' but row contains farm details."
		},		
		{
			'row_num': "10101",
			'data':{
				"filename_1": "MAF32-194-1_0001.tif",
				'filename_2': None,
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
			},
			'warning': "Row 10101: Form type is 'Cover' but row contains farm details."
		}
	]		


@pytest.fixture()
def valid_dates():
	return [
		"15 October 1941",
		"January 1942",
		"4 July 1942",
		"05 July 1942",
		"July 1941",
		"1943",
		"01/05/1942",
		"6-6-1942",
		"12.12.1943",
		"1/1/42",
		"6 Jun",
		"03 February",
		"Sep",
		"November",
	]
	


@pytest.fixture()
def normalized_dates():
	return [
		"15 October 1941",
		"January 1942",
		"4 July 1942",
		"5 July 1942",
		"July 1941",
		"1943",
		"1 May 1942",
		"6 June 1942",
		"12 December 1943",
		"1 January 1942",
		"6 June",
		"3 February",
		"September",
		"November",
	]
	

@pytest.fixture()
def dates_with_invalid_format():
	return {
		'data': [
			"10 1942",
			"4th July 1942",
			"5th 1943",
		],
		'message': " is not a valid format. Further date checks cannot be performed.",
	}

@pytest.fixture()
def dates_outside_survey_range():
	return {
		'data': [
			"September 1945",	
			"31 October 1940",
		],
		'message': " is outside the survey timespan.",
	}


@pytest.fixture()
def invalid_calendar_dates():
	return {
		'data': [
			"32 March 1942",
			"29 February 1943",
			"30 February",
		],
		'message': " is not a valid calendar date."
	}


@pytest.fixture()
def farm_name():
	return({
		"1": ["[not specified]", "Holt Farm", "[not specified]", "[not specified]"], 
		"2": ["[not specified]", "Park Valley Farm", "[not specified]", "[not specified]"], 
		"3": ["Home Farm", "Serge Hill", "[not specified]", "[not specified]"],
		"4": ["Buckmans Farm etc", "Cuckmans Farm", "[not specified]", "[not specified]"],
		"5": ["Old Parkbury Farm", "Old Parkbury", "[not specified]", "[not specified]"],
		"6": ["[not specified]", "Netherwylde Farm", "[not specified]", "[not specified]"],
		"8": ["[not specified]", "Smug Oak Farm", "[not specified]", "[not specified]"],
		"9": ["[not specified]", "Garston Manor", "[not specified]", "[not specified]"],
		"10": ["[not specified]", "Silver Birches", "[not specified]", "[not specified]"],
		"11": ["[not specified]", "Spooners", "[not specified]", "[not specified]"],
		"12A": ["[not specified]", "Land at Ninnings Farm", "[not specified]", "[not specified]"],
		"12B": ["Millhouse Farm", "Millhouse Farm", "[not specified]", "[not specified]"],
		"13": ["[not specified]", "Harperbury", "[not specified]", "[not specified]"],
		"17": ["[not specified]", "Land at Park Street", "[not specified]", "[not specified]"],
		"18": ["[not specified]", "Home Farm", "[not specified]", "[not specified]"],
		"19": ["Little Munden Farm", "Little Munden Farm", "[not specified]", "[not specified]"],
		"20": ["Noke Farm", "Noke Farm", "[not specified]", "[not specified]"]
         })


@pytest.fixture()
def test():
	return({
		"1": ["Hill Top Farm", "Hilltop farm", "Hill top farm"],
		"2": ["Hill Top Farm", "Hilltop farm", "Hilltop farm"],
		"3": ["Hill Top Farm", "Hill top farm", "Hill Top farm"],
		"4": ["Hill Top Farm", "Hilltop farm"],
		"5": ["HillTop Farm", "Hilltop farm"]
		})


@pytest.fixture()
def test2():
	return({
		"1": ["Winstall Farm, South Normanton, Alfreton, Derbyshire", "South Normanton, near Alfreton, Derbyshire", "Winstall Farm, South Normanton, Alfreton, Derbyshire"]
		})


@pytest.fixture()
def test3():
	return({
		"1": ["c/o Mr S Fluck, Pilgrove Farm, Hayden Hill, Cheltenham", "Pilgrove Farm, Hayden Hill, Cheltenham", "c/o Mr G Fluck, Pilgrove Farm, Hayden Hill, Cheltenham, Gloucestershire"],
		"2": ["14, Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, London Road, Charlton Kings"],
		"3": ["14, Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, London Road, Charlton Kings", "The Laurels, London Road"],
		"4": ['Parkside, Frizington, Cumberland', 'Parkside Farm, Frizington', 'Parkside, Frizington, Cumberland']
        })


