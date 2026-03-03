from src.farm_setup import Farm, concatenate_instance, concatenate_forms
from src.farm_setup import normalize_date

def test_farm_dataclass_instantiation(capsys, farms):
	for farm_fixture in farms:
		new_farm = Farm(**farm_fixture)
		with capsys.disabled():
			print(f"{new_farm.catalogue_reference}")
			print(new_farm.forms)
		assert isinstance(new_farm, Farm)
            
def test_farm_attribute_concatenation(concatenation_data):
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
			assert concatenated_farm.owner.group_names == test_data['result']['owner_group_names']
		if farm_name == "1 Ashwell/4":
			assert concatenated_farm.addressee.address == test_data['result']['address']


def test_concatenate_forms(concatenate_forms_fixture):
	for index, farm_data in enumerate(concatenate_forms_fixture):
		existing_farm = farm_data[0]
		for new_farm in farm_data[1:]:
			existing_farm = concatenate_forms(existing_farm, new_farm)
		if index == 0:
			assert len(existing_farm['B496/EI']) == 2
			continue

		if index == 1:
			assert len(existing_farm['B496/EI'][0].images) == 3
			continue

def test_normalize_date(valid_dates, normalized_dates):
	for index, test_date in enumerate(valid_dates):
		expected_result = normalized_dates[index]

		assert expected_result == normalize_date(test_date)


