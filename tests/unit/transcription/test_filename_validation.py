from src._dataclasses.transcription_model import Transcription
from src.harvester.transcription_checker import TranscriptionChecker


def test_values_between_filenames_different_pieces(farm):
	farm.update({
		'filename_1': "MAF32-194-1_59.tif",
		'filename_2': "MAF32-195-1_60.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-194-1_59.tif and MAF32-195-1_60.tif have different pieces."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_values_between_filenames_different_parish_numbers(farm):
	farm.update({
		'filename_1': "MAF32-5-98_28.tif",
		'filename_2': "MAF32-5-96_29.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-5-98_28.tif and MAF32-5-96_29.tif have different parish numbers."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_values_between_filenames_image_number_error(farm):
	farm.update({
		'filename_2': "MAF32-167-28_388.tif",
		'filename_1': "MAF32-167-28_386.tif",
		'document_type': "C 47/SSY",
		'county': "CU Cumberland",
		'parish': "28 Aikton",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-167-28_386.tif and MAF32-167-28_388.tif are either not consecutive images or in the wrong order."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_values_between_filenames_parish_number_mismatch(farm):
	farm.update({
		'filename_1': "MAF32-5-96_28.tif",
		'filename_2': "MAF32-5-96_29.tif",
		'document_type': "B496/EI",
		'county': "HF Herefordshire",
		'parish': "98 Clehonger",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-5-96_28.tif and MAF32-5-96_29.tif have a different parish number from parish name '98 Clehonger'."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_not_consecutive_images(farm):
	farm.update({
		'filename_1': "MAF32-167-28_386.tif",
		'filename_2': "MAF32-167-28_385.tif",
		'document_type': "C 47/SSY",
		'county': "CU Cumberland",
		'parish': "28 Aikton",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._check_values_between_filenames()

	expected_message = f"{checker.row_prefix}MAF32-167-28_386.tif and MAF32-167-28_385.tif are either not consecutive images or in the wrong order."
	assert expected_message == checker.warnings['Filename Warnings'][0]

