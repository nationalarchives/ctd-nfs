from src._dataclasses.transcription_model import Transcription
from src._dataclasses.transcription_checker import TranscriptionChecker


def test_cover_image_inconsistencies_bad_cover_pattern(farm):
	farm.update({
		'filename_1': "MAF32-194-1_59.tif",
		'filename_2': "",
		'document_type': "Cover",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._report_cover_image_inconsistencies()

	expected_message = f"{checker.row_prefix}Form type is 'Cover' but MAF32-194-1_59.tif does not match expected cover pattern or have image number 0001."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_cover_with_two_images_1(farm):
	farm.update({
		'filename_1': "MAF32-193-203_97.tif",
		'filename_2': "MAF32-193-203_98.tif",
		'document_type': "Cover",
		'county': "CU Cumberland",
		'parish': "203 Winscales",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._report_cover_image_inconsistencies()

	expected_message = f"{checker.row_prefix}Form type is 'Cover' but two form images were provided: MAF32-193-203_97.tif and MAF32-193-203_98.tif."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_cover_with_two_images_2(farm):
	farm.update({
		'filename_1': "MAF32-51-285_0001.tif",
		'filename_2': "MAF32-51-285_0002.tif",
		'document_type': "Cover",
		'county': "WL Wiltshire",
		'parish': "285 Zeals",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._report_cover_image_inconsistencies()

	expected_message = f"{checker.row_prefix}Form type is 'Cover', and MAF32-51-285_0001.tif matches expected pattern for cover image but additional image MAF32-51-285_0002.tif was also provided."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_form_supplied_but_cover_image(farm):
	farm.update({
		'filename_1': "MAF32-51-285_0001.tif",
		'filename_2': "",
		'document_type': "SF",
		'county': "WL Wiltshire",
		'parish': "285 Zeals",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._report_cover_image_inconsistencies()

	expected_message = f"{checker.row_prefix}MAF32-51-285_0001.tif matches expected cover pattern or has image number 0001 but form type is 'SF'."
	assert expected_message == checker.warnings['Filename Warnings'][0]


def test_cover_image_inconsistencies_form_supplied_but_cover_pattern(farm):
	farm.update({
		'filename_1': "MAF32-51-285.tif",
		'filename_2': "",
		'document_type': "SF",
		'county': "WL Wiltshire",
		'parish': "285 Zeals",
	})
	transcription = Transcription(**farm)
	row_number = "10"

	checker = TranscriptionChecker(transcription=transcription, row_number=row_number)
	checker._report_cover_image_inconsistencies()

	expected_message = f"{checker.row_prefix}MAF32-51-285.tif matches expected cover pattern or has image number 0001 but form type is 'SF'."
	assert expected_message == checker.warnings['Filename Warnings'][0]

