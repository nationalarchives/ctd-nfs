import pytest


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
			"addressee_title": "",
			"addressee_individual_name": "",
			"addressee_group_names": "",
			"address": "",
			"owner_title": "Rev",
			"owner_individual_name": "H R Fleming",
			"owner_group_names": "*",
			"owner_address": "Rayrigg Hall, Windermere, Westmorland",
			"farmer_title": "*",
			"farmer_individual_name": "R Nicholson",
			"farmer_group_names": "*",
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
			"additional_farms": "",
			"farm_name": "",
			"addressee_title": "Mr",
			"addressee_individual_name": "W Parsons",
			"addressee_group_names": "*",
			"address": "Gale House, Ambleside, Westmorland",
			"owner_title": "",
			"owner_individual_name": "",
			"owner_group_names": "R T E Conant, Agents Smith and Co; The Crown, Carter Jonas and Sons; Rev Barston",
			"owner_address": "",
			"farmer_title": "",
			"farmer_individual_name": "",
			"farmer_group_names": "",
			"farmer_address": "",
			"acreage": "",
			"OS_map_sheet": "",
			"field_info_date": "",
			"primary_record_date": "",
		},
		{
			"filename_1": "MAF32-228-1_23.tif",
			"filename_2": "MAF32-228-1_24.tif",
			"document_type": "B496/EI",
			"county": "DM Durham",
			"parish": "1 Barnard Castle",
			"primary_farm_number": "4",
			"additional_farms": "",
			"farm_name": "9 King Street",
			"addressee_title": "",
			"addressee_individual_name": "",
			"addressee_group_names": "",
			"address": "",
			"owner_title": "*",
			"owner_individual_name": "*",
			"owner_group_names": "Mr Kellett; Mr Swift; Mr W Bain; Mrs Mane; Mrs Todd; W Walton",
			"owner_address": "8 Sendal, Yorkshire; Barnard Castle; Darlington Road, Barnard Castle; Gallowgate, Barnard Castle; Gallowgate, Barnard Castle; 24 Coronation Road, Redcar",
			"farmer_title": "*",
			"farmer_individual_name": "W J Chaplow",
			"farmer_group_names": "*",
			"farmer_address": "Barnard Castle",
			"acreage": "30/Nil Acres",
			"OS_map_sheet": "XL NE 1898",
			"field_info_date": "*",
			"primary_record_date": "19 April 1943",
		},
		{
			"filename_1": "MAF32-247-23_75.tif",
			"filename_2": "MAF32-247-23_76.tif",
			"document_type": "B496/EI",
			"county": "RD Rutland",
			"parish": "23 Hambleton",
			"primary_farm_number": "19",
			"additional_farms": "",
			"farm_name": "Armley Lodge",
			"addressee_title": "",
			"addressee_individual_name": "",
			"addressee_group_names": "",
			"address": "",
			"owner_title": "*",
			"owner_individual_name": "*",
			"owner_group_names": "Nichols, Agent for the Earl of Ancaster",
			"owner_address": "Hambleton, Oakham",
			"farmer_title": "*",
			"farmer_individual_name": "*",
			"farmer_group_names": "Woodhead Bros",
			"farmer_address": "Hambleton, Oakham",
			"acreage": "Arable 127.5; Grass 45; 172.5",
			"OS_map_sheet": "9 NE1931 Edition",
			"field_info_date": "30 January 1942",
			"primary_record_date": "*"
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
					'additional_farms': "",
					'farm_name': "Glebe Farm",
					'addressee_title': "*",
					'addressee_individual_name': "*",
					'addressee_group_names': "A Lane and C Lane",
					'address': "Burley, Oakham, Rutland",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
				{
					'filename_1': "MAF32-346-10_27.tif",
					'filename_2': "MAF32-346-10_28.tif",
					'document_type': "B496/EI",
					'county': "RD Rutland",
					'parish': "10 Burley",
					'primary_farm_number': "7",
					'additional_farms': "",
					'farm_name': "*",
					'addressee_title': "",
					'addressee_individual_name': "",
					'addressee_group_names': "",
					'address': "",
					'owner_title': "*",
					'owner_individual_name': "*",
					'owner_group_names': "Burley Estate",
					'owner_address': "*",
					'farmer_title': "*",
					'farmer_individual_name': "*",
					'farmer_group_names': "A Lane and C Lane",
					'farmer_address': "Burley, Oakham, Rutland",
					'acreage': "168 ac",
					'OS_map_sheet': "V 15",
					'field_info_date': "September 1942",
					'primary_record_date': "*",
				},
			],
			'result': "Glebe Farm",
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
					'additional_farms': "",
					'farm_name': "",
					'addressee_title': "*",
					'addressee_individual_name': "*",
					'addressee_group_names': "Rutland WAEC",
					'address': "Lodge Farm, Tickencote, Stamford, Lincolnshire",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
				{
					'filename_1': "MAF32-348-49_25.tif",
					'filename_2': "MAF32-348-49_26.tif",
					'document_type': "C 47/SSY",
					'county': "RD Rutland",
					'parish': "49 Tickencote",
					'primary_farm_number': "6",
					'additional_farms': "",
					'farm_name': "",
					'addressee_title': "*",
					'addressee_individual_name': "*",
					'addressee_group_names': "The Rutland War Agricultural Committee",
					'address': "Lodge Farm, Tickencote, Stamford, Lincolnshire",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
			],
			'result': ["Rutland WAEC", "The Rutland War Agricultural Committee"],
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
					'additional_farms': "",
					'farm_name': "*",
					'addressee_title': "Mr",
					'addressee_individual_name': "W Mitchell",
					'addressee_group_names': "*",
					'address': "Waste Lane, Cockermouth",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
				{
					'filename_1': "MAF32-176-100_221.tif",
					'filename_2': "MAF32-176-100_222.tif",
					'document_type': "C 47/SSY",
					'county': "CU Cumberland",
					'parish': "96 Cockermouth",
					'primary_farm_number': "10",
					'additional_farms': "",
					'farm_name': "",
					'addressee_title': "Mr",
					'addressee_individual_name': "Wm Mitchell",
					'addressee_group_names': "*",
					'address': "Dairyman, Cockermouth, Cumberland",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
			],
			'result': "*"
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
					'additional_farms': "",
					'farm_name': "Branthwaite Mill, North Workington",
					'addressee_title': "Mr",
					'addressee_individual_name': "Wm West",
					'addressee_group_names': "*",
					'address': "Branthwaite Mill, North Workington",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
				{
					'filename_1': "MAF32-175-97_237.tif",
					'filename_2': "MAF32-175-97_238.tif",
					'document_type': "B496/EI",
					'county': "CU Cumberland",
					'parish': "97 Dean",
					'primary_farm_number': "47",
					'additional_farms': "",
					'farm_name': "Branthwaite Mill",
					'addressee_title': "",
					'addressee_individual_name': "",
					'addressee_group_names': "",
					'address': "",
					'owner_title': "*",
					'owner_individual_name': "*",
					'owner_group_names': "*",
					'owner_address': "*",
					'farmer_title': "*",
					'farmer_individual_name': "Wm West",
					'farmer_group_names': "*",
					'farmer_address': "Branthwaite Mill, Branthwaite, Workington",
					'acreage': "35/-/35",
					'OS_map_sheet': "XLII 1926",
					'field_info_date': "27 August 1941",
					'primary_record_date': "*",
				},
			],
			'result': "Mr",
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
					'additional_farms': "",
					'farm_name': "*",
					'addressee_title': "Mr",
					'addressee_individual_name': "F Notley",
					'addressee_group_names': "*",
					'address': "Hillside Farm, Farmborough, Bath",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
				{
					'filename_1': "MAF32-134-296_53.tif",
					'filename_2': "MAF32-134-296_54.tif",
					'document_type': "B496/EI",
					'county': "ST Somerset",
					'parish': "296 Farmborough",
					'primary_farm_number': "14",
					'additional_farms': "",
					'farm_name': "Hillside Farm",
					'addressee_title': "",
					'addressee_individual_name': "",
					'addressee_group_names': "",
					'address': "",
					'owner_title': "*",
					'owner_individual_name': "*",
					'owner_group_names': ["F A C Notley", "Mrs Bridges"],
					'owner_address': ["Bloomfield, Timsbury", "Timsbury, Near Bath"],
					'farmer_title': "*",
					'farmer_individual_name': "L Gregory",
					'farmer_group_names': "*",
					'farmer_address': "Hillside Farm, Farmborough, Near Bath",
					'acreage': "50",
					'OS_map_sheet': "XIII SW 2nd Edition 1903",
					'field_info_date': "26/02/1944",
					'primary_record_date': "23/05/1944",
				},
			],
			'result': "Hillside Farm",
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
					'additional_farms': "",
					'farm_name': "Beasley Farm",
					'addressee_title': "*",
					'addressee_individual_name': "E I Kemp",
					'addressee_group_names': "*",
					'address': "High Street, Dulverton",
					'owner_title': "",
					'owner_individual_name': "",
					'owner_group_names': "",
					'owner_address': "",
					'farmer_title': "",
					'farmer_individual_name': "",
					'farmer_group_names': "",
					'farmer_address': "",
					'acreage': "",
					'OS_map_sheet': "",
					'field_info_date': "",
					'primary_record_date': "",
				},
				{
					'filename_1': "MAF32-131-91_137.tif",
					'filename_2': "MAF32-131-91_138.tif",
					'document_type': "B496/EI",
					'county': "ST Somerset",
					'parish': "91 Dulverton",
					'primary_farm_number': "26",
					'additional_farms': "",
					'farm_name': "High Street",
					'addressee_title': "",
					'addressee_individual_name': "",
					'addressee_group_names': "",
					'address': "",
					'owner_title': "*",
					'owner_individual_name': "*",
					'owner_group_names':["The Hon Mrs Herbert Pixton", "Hon Mrs Pixton", "Mr Abbott", "Mrs Surridge", "Miss Dowey"],
					'owner_address': ["Dulverton", "Dulverton", "The Cottage, Dulverton", "Exter", "Green Hotel, Dulverton"],
					'farmer_title': "*",
					'farmer_individual_name': "*",
					'farmer_group_names': "E S Kemp and Sons",
					'farmer_address': "High Street and Beasly Farm, Dulverton",
					'acreage': "",
					'OS_map_sheet': "LXVII NW 2nd Edition 1905",
					'field_info_date': "",
					'primary_record_date': "02/01/1944",
				},
			],
			'result': ["The Hon Mrs Herbert Pixton", "Hon Mrs Pixton", "Mr Abbott", "Mrs Surridge", "Miss Dowey"]
		},
	}



@pytest.fixture()
def bad_farm_initial_values():
	return	[
		{
			'data':{
				'row_num': '1111',
				"filename_1": "MAF32-194-1_59.tif",
				"filename_2": "MAF32-195-1_60.tif",
				"document_type": "C51/SSY",
				"county": "WD Westmorland",
				"parish": "1 Ambleside",
			},
			'warning': "Row 1111: MAF32-194-1_59.tif and MAF32-195-1_60.tif have different box numbers. Box number of MAF32-194-1_59.tif will be used in the catalogue reference."
		},
		{
			'data':{
				'row_num': '2222',
				"filename_1": "MAF32-5-98_28.tif",
				"filename_2": "MAF32-5-96_29.tif",
				"document_type": "B496/EI",
				"county": "HF Herefordshire",
				"parish": "98 Clehonger",
			},
			'warning': "Row 2222: MAF32-5-98_28.tif and MAF32-5-96_29.tif have different parish numbers. Parish number from full parish name '98 Clehonger' will be used in the catalogue reference."
		},
		{
			'data':{
				'row_num': '3333',
				"filename_1": "MAF32-194-1_59.tif",
				"filename_2": "",
				"document_type": "Cover",
				"county": "WD Westmorland",
				"parish": "1 Ambleside",
			},
			'warning': "Row 3333: Form type is 'Cover' but MAF32-194-1_59.tif does not match expected cover pattern or have image number 0001."
		},
		{
			'data':{
				'row_num': '4444',
				"filename_1": "MAF32-5-96_28.tif",
				"filename_2": "MAF32-5-96_29.tif",
				"document_type": "B496/EI",
				"county": "HF Herefordshire",
				"parish": "98 Clehonger",
			},
			'warning': "Row 4444: MAF32-5-96_28.tif and MAF32-5-96_29.tif have a diffeent parish number from parish name '98 Clehonger'. Parish number from full parish name will be used in the catalogue reference."
		},
		{
			'data':{
				'row_num': '5555',
				"filename_1": "MAF32-167-28_386.tif",
				"filename_2": "MAF32-167-28_388.tif",
				"document_type": "C 47/SSY",
				"county": "CU Cumberland",
				"parish": "28 Aikton",
			},
			'warning': "Row 5555: MAF32-167-28_386.tif and MAF32-167-28_388.tif are either not consecutive images or in the wrong order."
		},
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
		{
			'data':{
				'row_num': '7777',
				"filename_1": "MAF32-51-285_0001.tif",
				"filename_2": "",
				"document_type": "SF",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 7777: MAF32-51-285_0001.tif matches expected cover pattern or has image number 0001 but form type is 'SF'."
		},
		{
			'data':{
				'row_num': '8888',
				"filename_1": "MAF32-51-285_0001.tif",
				"filename_2": "MAF32-51-285_0002.tif",
				"document_type": "Cover",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 8888: Form type is 'Cover', and MAF32-51-285_0001.tif matches expected pattern for cover image but additional image MAF32-51-285_0002.tif was also provided."
		},
		{
			'data':{
				'row_num': '9999',
				"filename_1": "MAF32-51-285.tif",
				"filename_2": "",
				"document_type": "SF",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 9999: MAF32-51-285.tif matches expected cover pattern or has image number 0001 but form type is 'SF'."
		},
	]


@pytest.fixture()
def bad_form():
	return	[
				{
			'data':{
				'row_num': '10101',
				"filename_1": "MAF32-51-285.tif",
				"filename_2": "",
				"document_type": "SF47/SSY",
				"county": "WL Wiltshire",
				"parish": "285 Zeals",
			},
			'warning': "Row 10101: Form type 'SF47/SSY' is not a recognised form."
		},		
	]

@pytest.fixture()
def names1():
	return({
        "1": ["H Arkell", "H Arkell", "H Arkell", "H Arkell"], 
		"2": ["", "W H Buckle", "W H Buckle", "W H Buckle"], 
		"3": ["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"6": ["A E Cook", "A E Cook", "A E Cook", "A E Cook"],
		"7": ["A G Griffiths", "W L Edmunds", "W L Edmunds", "W L Edmunds"],
		"9": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"],
		"10": ["", "F W Hinton", "", "F W Hinton"],
		"14": ["G P Rymer", "G P Rymer", "G P Rymer", "G P Rymer"],
		"15": ["A Spragg", "A Spragg", "A Spragg", "A Spragg"],
		"16": ["H Bowl", "Harry Bowl", "H Bowl", "Harry Bowl"],
		"18": ["A Tombs", "A Tombs", "A Tombs", "A Tombs"],
		"19": ["C Tombs", "C Toombs", "C Toombs", "C Toombs"],
		"20": ["G O Tombs", "G O Tombs", "G O Tombs", "G O Tombs"],
		"22": ["G Wilkins", "G Wilkins", "Geo Wilkin", "G Wilkins"],
		"31": ["", "F Bendall", "F Bendall", "F Bendall"],
		"33": ["F Thomas", "Frank Thomas", "F. Thomas", "Frank Thomas"]
         })


@pytest.fixture()
def names2():
	return({
		"1": ["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"2": ["R Burroughs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"3": ["R Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"4": ["R Burroughs", "J Burroghs", "J Burroughs", "R Burroughs"], 
		"5": ["R J Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"],
		"6": ["J R Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"], 
		"7": ["J R Burrows", "J Burroughs", "J Burroughs", "J Burroughs"], 
		"8": ["R J Burroughs", "R L Burroughs", "R Burroughs", "R Burroughs"],
		"9": ["R J Burrows", "R L Burroughs", "J Burroughs", "J Burroughs"],
		"10": ["R J Burrows", "R L Burroughs", "R Burroughs", "R Burroughs"],
		"11": ["R Burrows", "R Burroughs", "R Burroughs", "F Rymer"],
		"12": ["R Burrows", "R Burroughs", "R Burroughs", "R Rymer"],
		"13": ["R Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
		"14": ["R Burrows", "R F Burroughs", "R Burroughs", "F Rymer"],
		"15": ["R J Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
		"16": ["R J Burrows", "R Burroughs", "R Burroughs", "R J Burroghs"],
		"17": ["R J Burrows", "A E Cook", "G P Rymer", "Geo Wilkin"],
		"18": ["R J Burrows", "R Burroughs", "G P Rymer", "Geo Wilkin"],
		"19": ["R J Burrows", "R Burroughs", "R Burroghs", "R J Burroghs"],
		"20": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"]                
        })


@pytest.fixture()
def names3():
	return({"1": ["Messrs Rowe and Raddy", "Mr A C Raddy for Rowe and Raddy"]})


@pytest.fixture()
def address():
	return({
		"1": ["Butlers Court Farm, Boddington, Gloucestershire", "Butlers Court, Boddington, Near Cheltenham", "Butlers Court, Boddington", "Butlers Court Farm, Boddington, Gloucestershire"], 
		"2": ["Whitehall, Hayden Hill, Cheltenham, Gloucestershire", "Whitehall Farm, Hayden, Cheltenham", "Whitehall Farm, Hayden, Cheltenham", "Whitehall, Hayden Hill, Cheltenham, Gloucestershire"], 
		"3": ["Boddington House Farm, Boddington, Gloucestershire", "Boddington House Farm, Boddington, Cheltenham", "Boddington House Farm, Near Cheltenham", "Boddington House, Boddington, Gloucestershire"],
		"6": ["Slate Mill, Boddington, Near Cheltenham, Gloucestershire","Slade Mill, Boddington, Cheltenham", "Slate Mill, Boddington", "Slate Mill, Boddington, Near Cheltenham, Gloucestershire"],
		"7": ["Barrow Court, Boddington, Cheltenham, Gloucestershire", "14, Foregate Street, Worcester", "Barrow Court, Boddington", "Barrow Court, Boddington, Cheltenham, Gloucestershire"],
		"9": ["Manor Farm, Boddington, Near Cheltenham, Gloucestershire", "Guiting House, Temple Guiting, Gloucestershire", "Manor Farm, Boddington", "Manor Farm, Boddington, Near Cheltenham, Gloucestershire"],
		"10": ["c/o Mr S Fluck, Pilgrove Farm, Hayden Hill, Cheltenham", "192 High Street, Cheltenham", "Pilgrove Farm, Hayden Hill, Cheltenham", "c/o Mr G Fluck, Pilgrove Farm, Hayden Hill, Cheltenham, Gloucestershire"],
		"14": ["14 Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, Charlton Kings, Cheltenham", "The Laurels, London Road, Charlton Kings", "The Laurels, London Road"],
		"15": ["Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire", "Mill House Farm, Boddington, Near Cheltenham", "Withybridge Farm, Boddington", "Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire"],
		"16": ["Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire", "Barrow Hill Farm, Boddington, Cheltenham", "Barrow Hill Farm, Boddington", "Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire"],
		"18": ["Brookes Laymes Farm, Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Brookes Laymes Farm, Boddington", "Brookes Laymes Farm, Boddington, Gloucestershire"],
		"19": ["Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Boddington", "Boddington, Gloucestershire"],
		"20": ["Hayden Farm, Boddington, Near Cheltenham, Gloucestershire", "Hayden Farm, Hayden, Cheltenham", "Hayden Farm, Boddington", "Hayden Farm, Boddington, Near Cheltenham, Gloucestershire"],
		"22": ["Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire", "Wilkins Farm, Boddington, Cheltenham", "Wilkins Farm, Barrow, Boddington", "Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire"],
		"31": ["1 Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire", "1 Hayden Hill Villas, Hayden Hill, Boddington", "Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire"],
		"33": ["Pilgrove, Hayden Hill, Near Cheltenham, Gloucestershire", "Pilgrove, Hayden Hill, Boddington, Gloucestershire", "Pilgrove, Hayden Hill, Cheltenham", "Pilgrove, Hayden Hilll, Near Cheltenham, Gloucestershire"],
		})


@pytest.fixture()
def farm_name():
	return({
		"1": ["*", "Holt Farm", "", ""], 
		"2": ["*", "Park Valley Farm", "", ""], 
		"3": ["Home Farm", "Serge Hill", "", ""],
		"4": ["Buckmans Farm etc", "Cuckmans Farm", "", ""],
		"5": ["Old Parkbury Farm", "Old Parkbury", "", ""],
		"6": ["*", "Netherwylde Farm", "", ""],
		"8": ["*", "Smug Oak Farm", "", ""],
		"9": ["*", "Garston Manor", "", ""],
		"10": ["*", "Silver Birches", "", ""],
		"11": ["*", "Spooners", "", ""],
		"12A": ["", "Land at Ninnings Farm", "", ""],
		"12B": ["Millhouse Farm", "Millhouse Farm", "", ""],
		"13": ["*", "Harperbury", "", ""],
		"17": ["*", "Land at Park Street", "", ""],
		"18": ["*", "Home Farm", "", ""],
		"19": ["Little Munden Farm", "Little Munden Farm", "", ""],
		"20": ["Noke Farm", "Noke Farm", "", ""]
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


