from src.farm_class_setup import Farm
from src.pre_instantiation_checks import perform_pre_instantiation_checks


def test_farm_dataclass_instantiation(farms):
    for farm_fixture in farms:
        new_farm = Farm(farm_fixture)        
        assert isinstance(new_farm, Farm)


def test_filename_pre_instantiation_checks_pass(bad_farm_initial_values):
	for test in bad_farm_initial_values:
		result = perform_pre_instantiation_checks(test['data'])
		assert test['warning'] == result['Filename Warnings'][0]


def test_form_pre_instantiation_checks_pass(bad_form):
	for test in bad_form:
		result = perform_pre_instantiation_checks(test['data'])
		assert test['warning'] == result['Type Warnings'][0]
            

