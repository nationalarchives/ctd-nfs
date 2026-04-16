import pytest

from src._dataclasses.transcription_model import Transcription
from src.harvester.transcriptions_processor import TranscriptionsProcessor


# @pytest.mark.skip(reason="awaiting refactoring of concatenation methods")
def test_concatenate_muliple_of_same_form(transcription):
	fixture1 = transcription.copy()
	fixture2 = transcription.copy()

	fixture1.update({
		'filename_1': "MAF32-167-29_1.tif",
		'filename_2': "MAF32-167-29_2.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	fixture2.update({
		'filename_1': "MAF32-167-29_23.tif",
		'filename_2': "MAF32-167-29_24.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription1 = Transcription(**fixture1)
	transcription2 = Transcription(**fixture2)

	processor = TranscriptionsProcessor(transcriptions=[transcription1, transcription2])
	forms = processor._concatenate_forms()

	expected_number_of_forms = 2
	assert expected_number_of_forms == len(forms)


def test_concatenate_consecutive_images_to_existing_form(transcription):
	fixture1 = transcription.copy()
	fixture2 = transcription.copy()

	fixture1.update({
		'filename_1': "MAF32-167-29_21.tif",
		'filename_2': "MAF32-167-29_22.tif",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	fixture2.update({
		'filename_1': "MAF32-167-29_23.tif",
		'filename_2': "",
		'document_type': "C51/SSY",
		'county': "WD Westmorland",
		'parish': "1 Ambleside",
	})
	transcription1 = Transcription(**fixture1)
	transcription2 = Transcription(**fixture2)

	processor = TranscriptionsProcessor(transcriptions=[transcription1, transcription2])
	forms = processor._concatenate_forms()

	expected_number_of_forms = 1
	assert expected_number_of_forms == len(forms)


@pytest.mark.skip(reason="awaiting refactoring of concatenation methods")
def test_farm_attribute_concatenation(concatenation_data):
	pass
	for farm_name, test_data in concatenation_data.items():
		existing_farm = Farm(**test_data['data'][0])
		new_farm = Farm(**test_data['data'][1])
		concatenated_farm = concatenate_instance(existing_farm, new_farm)
		if farm_name == "10 Burley/7":
			assert concatenated_farm.farm_name == test_data['result']['farm_name']
		if farm_name == "49 Tickencote/6":
			assert concatenated_farm.addressee.group_names == test_data['result']['addressee_group_names']
		if farm_name == "96 Cockermouth/10":
			assert concatenated_farm.addressee.group_names == test_data['result']['addressee_group_names']
		if farm_name == "97 Dean/47":
			assert concatenated_farm.addressee.title == test_data['result']['addressee_title']
		if farm_name == "296 Farmborough/14":
			assert concatenated_farm.farm_name == test_data['result']['farm_name']
		if farm_name == "91 Dulverton/26":
			assert concatenated_farm.owner.address == test_data['result']['owner_address']
		if farm_name == "1 Ashwell/4":
			assert concatenated_farm.addressee.address == test_data['result']['address']


@pytest.mark.skip(reason="awaiting refactoring of concatenation methods")
def test_normalRize_date(valid_dates, normalized_dates):
	for index, test_date in enumerate(valid_dates):
		expected_result = normalized_dates[index]
		assert expected_result == _normalize_date(test_date)

