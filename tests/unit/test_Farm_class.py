import pytest

from src.farm_builder import Farm, concatenate_farms
# from src.pre_instantiation_checks import perform_pre_instantiation_checks


@pytest.mark.skip(reason="not required at this time")
def test_farm_dataclass_instantiation(farms):
    for farm_fixture in farms:
        new_farm = Farm(**farm_fixture)
        assert isinstance(new_farm, Farm)


@pytest.mark.skip(reason="test needs to be refactored to match new pre-instantiation check structure")
def test_filename_pre_instantiation_checks_pass(bad_farm_initial_values):
	for test in bad_farm_initial_values:
		_, warnings = perform_pre_instantiation_checks(test['data'])
		assert test['warning'] == warnings['Filename Warnings'][0]


@pytest.mark.skip(reason="test needs to be refactored to match new pre-instantiation check structure")
def test_form_pre_instantiation_checks_pass(bad_form):
	for test in bad_form:
		_, warnings = perform_pre_instantiation_checks(test['data'])
		assert test['warning'] == warnings['Type Warnings'][0]
            

@pytest.mark.skip
def test_farm_attribute_concatenation(concatenation_data):
	for farm_name, test_data in concatenation_data.items():
		existing_farm = Farm(**test_data['data'][0])
		new_farm = Farm(**test_data['data'][1])
		concatenated_farm = concatenate_farms(existing_farm, new_farm)
		if farm_name == "10 Burley/7":
			assert concatenated_farm.farm_name == test_data['result']['farm_name']
			assert dict(concatenated_farm.forms) == test_data['result']['forms']
		if farm_name == "49 Tickencote/6":
			assert concatenated_farm.addressee.group_names == test_data['result']['addressee_group_names']
			assert dict(concatenated_farm.forms) == test_data['result']['forms']
		if farm_name == "96 Cockermouth/10":
			assert concatenated_farm.addressee.group_names == test_data['result']['addressee_group_names']
			assert dict(concatenated_farm.forms) == test_data['result']['forms']
		if farm_name == "97 Dean/47":
			assert concatenated_farm.addressee.title == test_data['result']['addressee_title']
			assert dict(concatenated_farm.forms) == test_data['result']['forms']
		if farm_name == "296 Farmborough/14":
			assert concatenated_farm.farm_name == test_data['result']['farm_name']
			assert dict(concatenated_farm.forms) == test_data['result']['forms']
		if farm_name == "91 Dulverton/26":
			assert concatenated_farm.owner.group_names == test_data['result']['owner_group_names']
			assert dict(concatenated_farm.forms) == test_data['result']['forms']