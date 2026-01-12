import pytest

from src.farm_class_setup import Farm
from src.pre_instantiation_checks import perform_pre_instantiation_checks


def test_farm_dataclass_instantiation(farms):
    for farm_fixture in farms:
        new_farm = Farm(**farm_fixture)
        assert isinstance(new_farm, Farm)

@pytest.mark.skip()
def test_filename_pre_instantiation_checks_pass(bad_farm_initial_values):
	for test in bad_farm_initial_values:
		_, warnings = perform_pre_instantiation_checks(test['data'])
		assert test['warning'] == warnings['Filename Warnings'][0]

@pytest.mark.skip()
def test_form_pre_instantiation_checks_pass(bad_form):
	for test in bad_form:
		_, warnings = perform_pre_instantiation_checks(test['data'])
		assert test['warning'] == warnings['Type Warnings'][0]
            
