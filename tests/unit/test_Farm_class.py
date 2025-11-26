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
            

# def pre_instantiation_checks_passed(farms):
	# results = []
	# for farm in farms:
	# 	csv_values = {
	# 		'row_num': farms.index(farm) + 1,
	# 		'form': farm['document_type'],
	# 		'parish': farm['parish'],
	# 		'filename1': farm['filename_1'],
	# 		'filename2': farm['filename_2']
	# 	}
	# 	result = perform_pre_instantiation_checks(csv_values)
	# 	results.append(result)
	# return results

