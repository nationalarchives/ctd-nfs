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


def test_values_between_filenames_different_pieces():
	fixture.update({
		'filename_1': "MAF32-194-1_59.tif",
		'filename_2': "MAF32-195-1_60.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription = Transcription(**fixture)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-194-1_59.tif and MAF32-195-1_60.tif have different pieces."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_values_between_filenames_different_parish_numbers():
	fixture.update({
		'filename_1': "MAF32-5-98_28.tif",
		'filename_2': "MAF32-5-96_29.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription = Transcription(**fixture)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-5-98_28.tif and MAF32-5-96_29.tif have different parish numbers."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_values_between_filenames_image_number_error(values_between_filenames_image_number_error):
	fixture.update({
		'filename_2': "MAF32-167-28_388.tif",
		'filename_1': "MAF32-167-28_386.tif",
		'document_type': "C 47/SSY",
		'county': "CU Cumberland",
		'parish': "28 Aikton",
	})
	transcription = Transcription(**fixture)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-167-28_386.tif and MAF32-167-28_388.tif are either not consecutive images or in the wrong order."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_values_between_filenames_parish_number_mismatch(values_between_filenames_parish_number_mismatch):
	fixture.update({
		'filename_1': "MAF32-5-96_28.tif",
		'filename_2': "MAF32-5-96_29.tif",
		'document_type': "B496/EI",
		'county': "HF Herefordshire",
		'parish': "98 Clehonger",
	})
	transcription = Transcription(**fixture)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-5-96_28.tif and MAF32-5-96_29.tif have a different parish number from parish name '98 Clehonger'."
	assert expected_message == checker.warnings['Filename Warnings'][0]

